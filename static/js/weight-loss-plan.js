// Form validation and enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const form = document.querySelector('form.needs-validation');
    if (form) {
        // Weight range validation
        const weightInput = form.querySelector('input[name="weight"]');
        const targetWeightInput = form.querySelector('input[name="target_weight"]');
        const heightInput = form.querySelector('input[name="height"]');
        
        function validateNumberInput(input, min, max, fieldName) {
            input.addEventListener('input', function() {
                const value = parseFloat(this.value);
                let message = '';
                
                if (isNaN(value)) {
                    message = `الرجاء إدخال رقم صحيح`;
                } else if (value < min || value > max) {
                    message = `${fieldName} يجب أن يكون بين ${min} و ${max}`;
                }
                
                // Update validation message
                let feedback = this.parentElement.querySelector('.invalid-feedback');
                if (!feedback) {
                    feedback = document.createElement('div');
                    feedback.className = 'invalid-feedback';
                    this.parentElement.appendChild(feedback);
                }
                feedback.textContent = message;
                
                // Update validity state
                if (message) {
                    this.setCustomValidity(message);
                } else {
                    this.setCustomValidity('');
                }
            });
        }
        
        if (weightInput) validateNumberInput(weightInput, 30, 300, 'الوزن');
        if (targetWeightInput) validateNumberInput(targetWeightInput, 30, 300, 'الوزن المستهدف');
        if (heightInput) validateNumberInput(heightInput, 100, 250, 'الطول');
        
        // WhatsApp number formatting
        const whatsappInput = form.querySelector('input[name="whatsapp"]');
        if (whatsappInput) {
            whatsappInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.startsWith('20')) {
                    value = '+' + value;
                } else if (value.startsWith('01')) {
                    value = '+2' + value;
                } else if (value.length > 0 && !value.startsWith('+')) {
                    value = '+' + value;
                }
                e.target.value = value;
            });
        }
        
        // Form submission
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Scroll to first error
                const firstError = form.querySelector(':invalid');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
            form.classList.add('was-validated');
        });
    }
    
    // Results animations
    const statNumbers = document.querySelectorAll('.stat-number');
    if (statNumbers.length > 0) {
        const animateNumber = (element, target) => {
            const value = parseInt(target);
            const duration = 1000;
            const start = 0;
            const increment = (timestamp) => {
                if (!increment.start) increment.start = timestamp;
                const progress = timestamp - increment.start;
                const percentage = Math.min(progress / duration, 1);
                
                element.textContent = Math.floor(start + (value - start) * percentage);
                
                if (percentage < 1) {
                    requestAnimationFrame(increment);
                }
            };
            requestAnimationFrame(increment);
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = entry.target.textContent;
                    animateNumber(entry.target, target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        statNumbers.forEach(number => observer.observe(number));
    }
});

// WhatsApp number validation and formatting
function formatWhatsAppNumber(input) {
    let value = input.value.replace(/\D/g, '');
    
    // Egyptian number formatting
    if (value.length > 0) {
        if (value.startsWith('01')) {
            // Local Egyptian number
            value = '2' + value;
        } else if (value.startsWith('1') && value.length === 10) {
            // Egyptian number without leading 0
            value = '20' + value;
        } else if (!value.startsWith('20') && value.length >= 10) {
            // Assume Egyptian if no country code
            value = '20' + value;
        }
    }
    
    input.value = value;
}

// Form validation
function validateForm() {
    const form = document.querySelector('.needs-validation');
    if (!form) return;
    
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    validateForm();
    
    // WhatsApp input formatting
    const whatsappInput = document.querySelector('input[name="whatsapp"]');
    if (whatsappInput) {
        whatsappInput.addEventListener('input', function() {
            formatWhatsAppNumber(this);
        });
    }
    
    // Animate statistics
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(stat => {
        const finalValue = parseInt(stat.textContent);
        let currentValue = 0;
        const increment = finalValue / 50;
        
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= finalValue) {
                stat.textContent = finalValue;
                clearInterval(timer);
            } else {
                stat.textContent = Math.floor(currentValue);
            }
        }, 30);
    });
});
