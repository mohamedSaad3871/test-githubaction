// Workout Guide JavaScript - Interactive Features

// Global variables
let currentMuscleGroup = 'all';
let currentDifficulty = 'all';
let currentEquipment = 'all';
let currentSearch = '';
let exercises = [];
let filteredExercises = [];

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeWorkoutGuide();
    setupEventListeners();
    loadExercises();
    setupAnimations();
});

// DOM elements
const searchInput = document.querySelector('input[name="search"]');
const muscleFilter = document.querySelector('select[name="muscle_group"]');
const difficultyFilter = document.querySelector('select[name="difficulty"]');
const equipmentFilter = document.querySelector('select[name="equipment"]');
const exerciseGrid = document.getElementById('exerciseGrid');
const muscleTabs = document.querySelectorAll('.muscle-tab');
const exerciseCount = document.querySelector('.exercise-count');

// Initialize the workout guide
function initializeWorkoutGuide() {
    // Add fade-in animation to main sections
    const sections = document.querySelectorAll('.fade-in');
    sections.forEach((section, index) => {
        setTimeout(() => {
            section.style.opacity = '1';
            section.style.transform = 'translateY(0)';
        }, index * 200);
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize modals
    const modalElements = document.querySelectorAll('.modal');
    modalElements.forEach(modal => {
        new bootstrap.Modal(modal);
    });
    
    // Initialize filters
    currentSearch = '';
    currentMuscleGroup = '';
    currentDifficulty = '';
    currentEquipment = '';
}

// Setup event listeners
function setupEventListeners() {
    // Search input - prevent form submission
    if (searchInput) {
        searchInput.addEventListener('input', debounce(handleSearch, 300));
        const form = searchInput.closest('form');
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                handleSearch({ target: searchInput });
            });
        }
    }

    // Filter dropdowns - prevent form submission
    if (muscleFilter) {
        muscleFilter.addEventListener('change', function(e) {
            e.preventDefault();
            handleMuscleFilter(e);
        });
    }
    if (difficultyFilter) {
        difficultyFilter.addEventListener('change', function(e) {
            e.preventDefault();
            handleDifficultyFilter(e);
        });
    }
    if (equipmentFilter) {
        equipmentFilter.addEventListener('change', function(e) {
            e.preventDefault();
            handleEquipmentFilter(e);
        });
    }

    // Muscle tabs - prevent default link behavior
    muscleTabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            handleMuscleTab(e);
        });
    });

    // Exercise cards - reload after filtering
    const exerciseItems = document.querySelectorAll('.exercise-item');
    exerciseItems.forEach(item => {
        const card = item.querySelector('.exercise-card');
        if (card) {
            card.addEventListener('click', handleExerciseClick);
        }
    });

    // Muscle map interactions
    const muscleGroups = document.querySelectorAll('.muscle-group');
    muscleGroups.forEach(group => {
        group.addEventListener('click', handleMuscleMapClick);
        group.addEventListener('mouseenter', handleMuscleMapHover);
        group.addEventListener('mouseleave', handleMuscleMapLeave);
    });

    // Workout split accordions
    const splitCards = document.querySelectorAll('.split-card');
    splitCards.forEach(card => {
        card.addEventListener('click', handleSplitCardClick);
    });

    // Scroll animations
    window.addEventListener('scroll', handleScroll);
}

// Load exercises from the page data
function loadExercises() {
    const exerciseItems = document.querySelectorAll('.exercise-item');
    exercises = Array.from(exerciseItems).map(item => {
        const card = item.querySelector('.exercise-card');
        return {
            element: item,
            name: card?.querySelector('.exercise-title')?.textContent || '',
            nameEn: card?.querySelector('.exercise-subtitle')?.textContent || '',
            muscle: item.dataset.muscle || '',
            difficulty: card?.querySelector('.difficulty-badge')?.textContent?.toLowerCase() || '',
            equipment: card?.querySelector('.exercise-stats .stat-item:last-child span')?.textContent || '',
            description: card?.querySelector('.exercise-description p')?.textContent || ''
        };
    });
    
    filteredExercises = [...exercises];
    updateExerciseCount();
}

// Handle search functionality
function handleSearch(e) {
    currentSearch = e.target.value.toLowerCase().trim();
    filterExercises();
}

// Handle muscle group filter
function handleMuscleFilter(e) {
    currentMuscleGroup = e.target.value;
    updateMuscleTabsActive();
    filterExercises();
}

// Handle difficulty filter
function handleDifficultyFilter(e) {
    currentDifficulty = e.target.value;
    filterExercises();
}

// Handle equipment filter
function handleEquipmentFilter(e) {
    currentEquipment = e.target.value;
    filterExercises();
}

// Handle muscle tab clicks
function handleMuscleTab(e) {
    e.preventDefault();
    
    // Extract muscle group from href or use 'all' for main tab
    const href = e.currentTarget.getAttribute('href');
    let muscle = 'all';
    if (href && href.includes('muscle_group=')) {
        muscle = href.split('muscle_group=')[1];
    }
    
    // Update active tab
    muscleTabs.forEach(tab => tab.classList.remove('active'));
    e.currentTarget.classList.add('active');
    
    // Update filter
    currentMuscleGroup = muscle === 'all' ? '' : muscle;
    if (muscleFilter) {
        muscleFilter.value = currentMuscleGroup;
    }
    
    filterExercises();
    
    // Smooth scroll to exercises section
    const exercisesSection = document.getElementById('exercise-library');
    if (exercisesSection) {
        exercisesSection.scrollIntoView({ behavior: 'smooth' });
    }
}

// Handle exercise card clicks
function handleExerciseClick(e) {
    const card = e.target.closest('.exercise-card');
    if (!card) return;
    
    const exerciseId = card.dataset.exerciseId;
    if (exerciseId) {
        showExerciseModal(exerciseId);
    }
}

// Handle muscle map clicks
function handleMuscleMapClick(e) {
    const muscle = e.currentTarget.dataset.muscle;
    if (muscle) {
        // Update muscle filter
        currentMuscleGroup = muscle;
        if (muscleFilter) {
            muscleFilter.value = muscle;
        }
        
        // Update muscle tabs
        updateMuscleTabsActive();
        
        // Filter exercises
        filterExercises();
        
        // Scroll to exercises
        const exercisesSection = document.getElementById('exercises-section');
        if (exercisesSection) {
            exercisesSection.scrollIntoView({ behavior: 'smooth' });
        }
    }
}

// Handle muscle map hover
function handleMuscleMapHover(e) {
    const muscle = e.currentTarget.dataset.muscle;
    const label = e.currentTarget.querySelector('.muscle-label');
    if (label) {
        label.style.display = 'block';
    }
    
    // Show tooltip
    const tooltip = document.createElement('div');
    tooltip.className = 'muscle-tooltip';
    tooltip.textContent = getMuscleNameArabic(muscle);
    tooltip.style.cssText = `
        position: absolute;
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
        pointer-events: none;
        z-index: 1000;
        transform: translate(-50%, -100%);
        margin-top: -10px;
    `;
    
    e.currentTarget.appendChild(tooltip);
}

// Handle muscle map leave
function handleMuscleMapLeave(e) {
    const tooltip = e.currentTarget.querySelector('.muscle-tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

// Handle workout split card clicks
function handleSplitCardClick(e) {
    const card = e.currentTarget;
    const details = card.querySelector('.split-details');
    
    if (details) {
        const isExpanded = details.style.display === 'block';
        
        // Close all other details
        document.querySelectorAll('.split-details').forEach(detail => {
            detail.style.display = 'none';
        });
        
        // Toggle current details
        details.style.display = isExpanded ? 'none' : 'block';
        
        // Add animation
        if (!isExpanded) {
            details.style.opacity = '0';
            details.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                details.style.transition = 'all 0.3s ease';
                details.style.opacity = '1';
                details.style.transform = 'translateY(0)';
            }, 10);
        }
    }
}

// Handle scroll animations
function handleScroll() {
    const elements = document.querySelectorAll('.slide-up');
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
            element.classList.add('animate');
        }
    });
}

// Filter exercises based on current filters
function filterExercises() {
    filteredExercises = exercises.filter(exercise => {
        const matchesSearch = !currentSearch || 
            exercise.name.toLowerCase().includes(currentSearch) ||
            exercise.nameEn.toLowerCase().includes(currentSearch) ||
            exercise.description.toLowerCase().includes(currentSearch);
        
        const matchesMuscle = !currentMuscleGroup || currentMuscleGroup === 'all' || exercise.muscle === currentMuscleGroup;
        const matchesDifficulty = !currentDifficulty || currentDifficulty === 'all' || exercise.difficulty.includes(currentDifficulty.toLowerCase());
        const matchesEquipment = !currentEquipment || currentEquipment === 'all' || exercise.equipment.toLowerCase().includes(currentEquipment.toLowerCase());
        
        return matchesSearch && matchesMuscle && matchesDifficulty && matchesEquipment;
    });
    
    displayFilteredExercises();
    updateExerciseCount();
}

// Display filtered exercises
function displayFilteredExercises() {
    exercises.forEach(exercise => {
        const isVisible = filteredExercises.includes(exercise);
        exercise.element.style.display = isVisible ? 'block' : 'none';
        
        if (isVisible) {
            exercise.element.classList.add('fade-in');
        }
    });
    
    // Show no results message if needed
    const noResults = document.getElementById('noResults');
    if (noResults) {
        noResults.style.display = filteredExercises.length === 0 ? 'block' : 'none';
    }
}

// Update exercise count
function updateExerciseCount() {
    if (exerciseCount) {
        exerciseCount.textContent = filteredExercises.length;
    }
    
    // Also update the results text if it exists
    const resultsText = document.querySelector('.results-text');
    if (resultsText) {
        resultsText.textContent = `عرض ${filteredExercises.length} من ${exercises.length} تمرين`;
    }
}

// Update muscle tabs active state
function updateMuscleTabsActive() {
    muscleTabs.forEach(tab => {
        tab.classList.toggle('active', tab.dataset.muscle === currentMuscleGroup);
    });
}

// Show exercise modal
function showExerciseModal(exerciseId) {
    const modal = document.getElementById(`exerciseModal${exerciseId}`);
    if (modal) {
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        
        // Load exercise details if needed
        loadExerciseDetails(exerciseId);
    }
}

// Load exercise details for modal
function loadExerciseDetails(exerciseId) {
    // This would typically fetch from an API
    // For now, we'll use the data already in the DOM
    console.log('Loading details for exercise:', exerciseId);
}

// Get Arabic muscle name
function getMuscleNameArabic(muscle) {
    const muscleNames = {
        'chest': 'الصدر',
        'back': 'الظهر',
        'shoulders': 'الأكتاف',
        'arms': 'الذراعين',
        'legs': 'الأرجل',
        'core': 'البطن'
    };
    return muscleNames[muscle] || muscle;
}

// Setup animations
function setupAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animatedElements = document.querySelectorAll('.slide-up, .fade-in');
    animatedElements.forEach(el => observer.observe(el));
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Smooth scroll to section
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Reset all filters
function resetFilters() {
    currentMuscleGroup = 'all';
    currentDifficulty = 'all';
    currentEquipment = 'all';
    currentSearch = '';
    
    if (searchInput) searchInput.value = '';
    if (muscleFilter) muscleFilter.value = 'all';
    if (difficultyFilter) difficultyFilter.value = 'all';
    if (equipmentFilter) equipmentFilter.value = 'all';
    
    muscleTabs.forEach(tab => tab.classList.remove('active'));
    
    filterExercises();
}

// Export functions for global access
window.WorkoutGuide = {
    scrollToSection,
    resetFilters,
    showExerciseModal,
    filterByMuscle: (muscle) => {
        currentMuscleGroup = muscle;
        updateMuscleTabsActive();
        filterExercises();
    }
};

// Progress tracking
class ProgressTracker {
    constructor() {
        this.completedExercises = new Set();
        this.loadProgress();
    }
    
    markComplete(exerciseId) {
        this.completedExercises.add(exerciseId);
        this.saveProgress();
        this.updateUI(exerciseId);
    }
    
    markIncomplete(exerciseId) {
        this.completedExercises.delete(exerciseId);
        this.saveProgress();
        this.updateUI(exerciseId);
    }
    
    isComplete(exerciseId) {
        return this.completedExercises.has(exerciseId);
    }
    
    saveProgress() {
        localStorage.setItem('workoutProgress', JSON.stringify([...this.completedExercises]));
    }
    
    loadProgress() {
        const saved = localStorage.getItem('workoutProgress');
        if (saved) {
            this.completedExercises = new Set(JSON.parse(saved));
        }
    }
    
    updateUI(exerciseId) {
        const card = document.querySelector(`[data-exercise-id="${exerciseId}"]`);
        if (card) {
            card.classList.toggle('completed', this.isComplete(exerciseId));
        }
    }
    
    getProgress(muscleGroup = null) {
        if (!muscleGroup) {
            return {
                completed: this.completedExercises.size,
                total: exercises.length,
                percentage: exercises.length > 0 ? (this.completedExercises.size / exercises.length) * 100 : 0
            };
        }
        
        const muscleExercises = exercises.filter(ex => ex.muscle === muscleGroup);
        const completed = muscleExercises.filter(ex => this.isComplete(ex.element.dataset.exerciseId)).length;
        
        return {
            completed,
            total: muscleExercises.length,
            percentage: muscleExercises.length > 0 ? (completed / muscleExercises.length) * 100 : 0
        };
    }
}

// Initialize progress tracker
const progressTracker = new ProgressTracker();
window.ProgressTracker = progressTracker;

// Tips and notifications
class TipManager {
    constructor() {
        this.tips = [
            'تذكر أن الإحماء مهم قبل بدء التمرين',
            'اشرب الماء بانتظام أثناء التمرين',
            'ركز على الشكل الصحيح أكثر من الوزن',
            'خذ راحة كافية بين المجموعات',
            'استمع لجسمك وتوقف عند الشعور بالألم'
        ];
        this.currentTipIndex = 0;
    }
    
    showRandomTip() {
        const randomIndex = Math.floor(Math.random() * this.tips.length);
        this.showTip(this.tips[randomIndex]);
    }
    
    showTip(message) {
        const toast = document.createElement('div');
        toast.className = 'toast-tip';
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas fa-lightbulb"></i>
                <span>${message}</span>
                <button class="toast-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            z-index: 9999;
            max-width: 300px;
            animation: slideInRight 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.animation = 'slideOutRight 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }
        }, 5000);
    }
}

const tipManager = new TipManager();
window.TipManager = tipManager;

// Show tip on page load
setTimeout(() => {
    tipManager.showRandomTip();
}, 3000);

// Add CSS for toast animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .toast-content {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .toast-close {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        margin-right: auto;
    }
    
    .exercise-card.completed {
        border: 2px solid #27ae60;
        background: linear-gradient(135deg, rgba(39, 174, 96, 0.1) 0%, rgba(39, 174, 96, 0.05) 100%);
    }
    
    .exercise-card.completed::after {
        content: '✓';
        position: absolute;
        top: 10px;
        left: 10px;
        background: #27ae60;
        color: white;
        width: 25px;
        height: 25px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: bold;
    }
`;
document.head.appendChild(style);