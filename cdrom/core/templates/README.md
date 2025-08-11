# Templates V2 - Modern Bootstrap 5.3.7 Templates

This is a complete set of modern, minimal, and beautiful HTML/Jinja2 templates for the Academia Python education platform.

## 🎨 Design Philosophy

- **Minimalist**: Clean, uncluttered design focused on content
- **Modern**: Latest Bootstrap 5.3.7 with contemporary design patterns
- **Responsive**: Mobile-first approach, works perfectly on all devices
- **Accessible**: Semantic HTML and proper ARIA attributes
- **Fast**: No JavaScript dependencies, pure CSS animations

## 🚀 Features

- ✅ Bootstrap 5.3.7 (latest version)
- ✅ Bootstrap Icons for consistent iconography
- ✅ Custom CSS variables for easy theming
- ✅ Responsive navigation with mobile hamburger menu
- ✅ Modern card-based layouts
- ✅ Smooth hover animations and transitions
- ✅ Professional color scheme optimized for education
- ✅ SEO-friendly structure with proper meta tags
- ✅ Form validation and enhanced UX
- ✅ No JavaScript required (except Bootstrap's own JS)

## 📁 Structure

```
templates_v2/
├── base.html                 # Main layout template
├── components/
│   ├── navbar.html          # Navigation component
│   └── footer.html          # Footer component
└── pages/
    ├── home.html            # Homepage
    ├── curso_list.html      # Course listing
    ├── curso_detail.html    # Course details
    ├── curso_form.html      # Course creation form
    ├── institucion_list.html # Institution listing
    ├── aula_list.html       # Classroom listing
    └── profe_list.html      # Teacher listing
```

## 🎨 Color Scheme

```css
:root {
    --primary-color: #3b82f6;    /* Blue */
    --secondary-color: #1e40af;  /* Dark Blue */
    --accent-color: #fbbf24;     /* Yellow */
    --success-color: #10b981;    /* Green */
    --text-primary: #1f2937;     /* Dark Gray */
    --text-secondary: #6b7280;   /* Medium Gray */
    --background-light: #f8fafc; /* Light Gray */
    --background-white: #ffffff; /* White */
    --border-color: #e5e7eb;     /* Light Border */
}
```

## 🚀 Getting Started

### 1. Update Django Settings

Add the new template directory to your Django settings:

```python
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates_v2'),  # Add this line
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.app_base_context',
            ],
        },
    },
]
```

### 2. Update Views

Update your views to use the new templates:

```python
# views.py
class HomePage(TemplateView):
    template_name = 'pages/home.html'

class CursoListView(ListView):
    model = Curso
    template_name = 'pages/curso_list.html'
    context_object_name = "lista"

class CursoDetailView(DetailView):
    model = Curso
    template_name = 'pages/curso_detail.html'
    context_object_name = "curso"

# And so on for other views...
```

### 3. Context Processors

Make sure your context processor provides the necessary variables:

```python
# core/context_processors.py
def app_base_context(request):
    return {
        'app_version': settings.APP_VERSION,
        'site_brand': settings.APP_LABEL,
        'site_email': settings.APP_EMAIL,
        'site_url': settings.APP_URL,
        'site_title': 'Academia Python - Aprende Desarrollo Web',
    }
```

## 📱 Responsive Design

All templates are fully responsive and include:

- Mobile-first CSS approach
- Collapsible navigation for mobile devices
- Responsive grid layouts
- Touch-friendly buttons and interactions
- Optimized typography for all screen sizes

## 🎯 Key Components

### Navigation
- Sticky navigation bar
- Mobile hamburger menu
- Active page highlighting
- Icon integration
- Dropdown menus for sub-sections

### Cards
- Hover effects with smooth transitions
- Consistent spacing and typography
- Image optimization
- Badge systems for status/categories

### Forms
- Enhanced form styling
- Client-side validation
- Helpful form text and tooltips
- Responsive form layouts

### Footer
- Multi-column layout
- Newsletter subscription
- Social media links
- Contact information
- Site map links

## 🔧 Customization

### Colors
Modify the CSS custom properties in `base.html`:

```css
:root {
    --primary-color: #your-color;
    --accent-color: #your-accent;
    /* ... other variables */
}
```

### Typography
The templates use system fonts for better performance:

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
```

### Icons
Using Bootstrap Icons CDN. You can replace with your preferred icon set.

## 🌟 Template Features

### Home Page (`pages/home.html`)
- Hero section with call-to-action
- Feature highlights
- Course preview
- Statistics section
- Newsletter signup

### Course List (`pages/curso_list.html`)
- Grid layout with course cards
- Filter options
- Course badges and metadata
- Empty state handling

### Course Detail (`pages/curso_detail.html`)
- Detailed course information
- Curriculum accordion
- Enrollment sidebar
- Project showcase
- Contact information

### Forms (`pages/curso_form.html`)
- Enhanced form styling
- Validation feedback
- Help text and tooltips
- Responsive layout

## 🚀 Performance

- No external fonts (system fonts only)
- Optimized CSS with minimal custom styles
- Bootstrap 5.3.7 from CDN
- No jQuery dependency
- Minimal custom JavaScript

## 📚 Usage Examples

### Extending Templates
```html
{% extends "base.html" %}

{% block title %}Your Page Title{% endblock %}

{% block content %}
<!-- Your content here -->
{% endblock %}

{% block extra_css %}
<style>
    /* Your custom CSS */
</style>
{% endblock %}
```

### Using Components
```html
<!-- Navigation is automatically included in base.html -->
{% include "components/navbar.html" %}

<!-- Footer is automatically included in base.html -->
{% include "components/footer.html" %}
```

## 🔄 Migration from Old Templates

1. Backup your current templates
2. Update your views to use new template paths
3. Test each page thoroughly
4. Update any custom template tags or filters
5. Adjust context processors if needed

## 🎓 Best Practices

1. **Consistent Naming**: Use descriptive file names
2. **Component Reuse**: Create reusable template components
3. **Performance**: Optimize images and minimize custom CSS
4. **Accessibility**: Use semantic HTML and proper ARIA labels
5. **SEO**: Include proper meta tags and structured data

## 🆘 Support

For questions or issues with these templates:

1. Check the Django documentation for template usage
2. Review Bootstrap 5.3.7 documentation for component options
3. Contact the development team

---

**Built with ❤️ for Academia Python**
*Modern, Beautiful, Responsive Education Platform*
