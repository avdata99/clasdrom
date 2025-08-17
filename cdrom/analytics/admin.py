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

        # Get statistics for the last 24 hours
        last_24h = timezone.now() - timedelta(hours=24)
        stats = RequestLog.objects.filter(timestamp__gte=last_24h).aggregate(
            total_requests=Count('id'),
            unique_ips=Count('ip_address', distinct=True),
            unique_users=Count('user', distinct=True),
        )

        extra_context['stats'] = stats
        return super().changelist_view(request, extra_context)

    def has_add_permission(self, request):
        """Disable adding records manually"""
        return False

    def has_change_permission(self, request, obj=None):
        """Make records read-only"""
        return False
