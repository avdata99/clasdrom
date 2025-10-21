from django.contrib import admin
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from analytics.models import RequestLog


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = [
        'timestamp', 'method', 'path_short',
        'ip_address', 'response_status', 'response_time_ms'
    ]
    list_filter = [
        'method', 'response_status', 'timestamp',
        ('user', admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = ['path', 'ip_address', 'user__username', 'user_agent']
    readonly_fields = [
        'timestamp', 'user', 'ip_address', 'user_agent', 'method',
        'url', 'path', 'query_string', 'referer', 'response_status',
        'response_time_ms'
    ]
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
    list_per_page = 50

    def path_short(self, obj):
        """Display shortened path"""
        if len(obj.path) > 50:
            return obj.path[:47] + '...'
        return obj.path
    path_short.short_description = 'Path'

    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('user')

    def changelist_view(self, request, extra_context=None):
        """Add statistics to the changelist view"""
        extra_context = extra_context or {}

        # Get statistics for the lastest days
        days = 3
        last_days = timezone.now() - timedelta(days=days)

        # Base queryset excluding admin paths and errors
        base_qs = RequestLog.objects.filter(
            timestamp__gte=last_days,
            response_status=200,  # Only successful requests
        ).exclude(
            path__startswith='/admin/'  # Exclude admin requests
        )

        # Daily statistics for the last days
        daily_stats = []
        for i in range(days):
            day_start = (timezone.now() - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)

            day_requests = base_qs.filter(
                timestamp__gte=day_start,
                timestamp__lt=day_end
            )

            total_requests = day_requests.count()
            unique_visitors = day_requests.values('ip_address').distinct().count()

            daily_stats.append({
                'date': day_start.date(),
                'requests': total_requests,
                'visitors': unique_visitors,
            })

        # Reverse to show oldest first
        daily_stats.reverse()

        # Calculate max values for chart scaling
        max_requests = max([day['requests'] for day in daily_stats]) or 1
        max_visitors = max([day['visitors'] for day in daily_stats]) or 1

        # Add chart data (simple percentage for bar width)
        for day in daily_stats:
            day['requests_width'] = int((day['requests'] / max_requests) * 100) if max_requests > 0 else 0
            day['visitors_width'] = int((day['visitors'] / max_visitors) * 100) if max_visitors > 0 else 0

        # URL-specific statistics
        # Get top 10 most visited URLs in the last days
        top_urls = base_qs.values('path').annotate(
            total_requests=Count('id'),
            unique_visitors=Count('ip_address', distinct=True)
        ).order_by('-total_requests')[:10]

        url_stats = []
        for url_data in top_urls:
            url_path = url_data['path']
            url_daily_stats = []

            for i in range(days):
                day_start = (timezone.now() - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
                day_end = day_start + timedelta(days=1)

                day_url_requests = base_qs.filter(
                    path=url_path,
                    timestamp__gte=day_start,
                    timestamp__lt=day_end
                )

                requests_count = day_url_requests.count()
                visitors_count = day_url_requests.values('ip_address').distinct().count()

                url_daily_stats.append({
                    'date': day_start.date(),
                    'requests': requests_count,
                    'visitors': visitors_count,
                })

            url_daily_stats.reverse()

            # Calculate max values for this URL's chart scaling
            url_max_requests = max([day['requests'] for day in url_daily_stats]) or 1
            url_max_visitors = max([day['visitors'] for day in url_daily_stats]) or 1

            # Add chart data
            for day in url_daily_stats:
                day['requests_width'] = int((day['requests'] / url_max_requests) * 100) if url_max_requests > 0 else 0
                day['visitors_width'] = int((day['visitors'] / url_max_visitors) * 100) if url_max_visitors > 0 else 0

            # Shorten URL path for display
            display_path = url_path
            if len(display_path) > 40:
                display_path = display_path[:37] + '...'

            url_stats.append({
                'path': url_path,
                'display_path': display_path,
                'total_requests': url_data['total_requests'],
                'total_visitors': url_data['unique_visitors'],
                'daily_stats': url_daily_stats,
                'max_requests': url_max_requests,
                'max_visitors': url_max_visitors,
            })

        # Overall statistics for the last 24 hours (keeping existing functionality)
        last_24h = timezone.now() - timedelta(hours=24)
        stats_24h = base_qs.filter(timestamp__gte=last_24h).aggregate(
            total_requests=Count('id'),
            unique_ips=Count('ip_address', distinct=True),
        )

        extra_context.update({
            'daily_stats': daily_stats,
            'url_stats': url_stats,
            'stats_24h': stats_24h,
            'max_requests': max_requests,
            'max_visitors': max_visitors,
        })
        return super().changelist_view(request, extra_context)

    def has_add_permission(self, request):
        """Disable adding records manually"""
        return False

    def has_change_permission(self, request, obj=None):
        """Make records read-only"""
        return False
