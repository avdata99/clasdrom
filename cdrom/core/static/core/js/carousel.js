class Carousel {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.slides = this.container.querySelector('.carousel-slides');
        this.slideElements = this.container.querySelectorAll('.carousel-slide');
        this.prevBtn = this.container.querySelector('.carousel-prev');
        this.nextBtn = this.container.querySelector('.carousel-next');
        this.indicators = this.container.querySelectorAll('.carousel-indicator');
        
        this.currentSlide = 0;
        this.totalSlides = this.slideElements.length;
        
        this.init();
    }
    
    init() {
        this.updateSlidePosition();
        this.updateIndicators();
        
        this.prevBtn.addEventListener('click', () => this.prevSlide());
        this.nextBtn.addEventListener('click', () => this.nextSlide());
        
        this.indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', () => this.goToSlide(index));
        });
        
        // Auto-play (optional)
        setInterval(() => this.nextSlide(), 5000);
    }
    
    updateSlidePosition() {
        const translateX = -this.currentSlide * 100;
        this.slides.style.transform = `translateX(${translateX}%)`;
    }
    
    updateIndicators() {
        this.indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === this.currentSlide);
        });
    }
    
    nextSlide() {
        this.currentSlide = (this.currentSlide + 1) % this.totalSlides;
        this.updateSlidePosition();
        this.updateIndicators();
    }
    
    prevSlide() {
        this.currentSlide = (this.currentSlide - 1 + this.totalSlides) % this.totalSlides;
        this.updateSlidePosition();
        this.updateIndicators();
    }
    
    goToSlide(index) {
        this.currentSlide = index;
        this.updateSlidePosition();
        this.updateIndicators();
    }
}

// Initialize carousels when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const carousels = document.querySelectorAll('.carousel-container');
    carousels.forEach((carousel, index) => {
        carousel.id = carousel.id || `carousel-${index}`;
        new Carousel(carousel.id);
    });
});
