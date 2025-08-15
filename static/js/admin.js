// Admin Dashboard JavaScript

class AdminDashboard {
    constructor() {
        this.init();
        this.bindEvents();
        this.loadSettings();
    }

    init() {
        // Initialize tooltips
        this.initTooltips();
        
        // Initialize sidebar
        this.initSidebar();
        
        // Initialize theme
        this.initTheme();
        
        // Initialize real-time updates
        this.initRealTimeUpdates();
    }

    initTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    initSidebar() {
        const sidebar = document.querySelector('.admin-sidebar');
        const main = document.querySelector('.admin-main');
        const toggleBtn = document.querySelector('.sidebar-toggle');

        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                sidebar.classList.toggle('collapsed');
                main.classList.toggle('expanded');
                localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
            });
        }

        // Restore sidebar state
        const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        if (isCollapsed) {
            sidebar.classList.add('collapsed');
            main.classList.add('expanded');
        }

        // Mobile sidebar toggle
        const mobileToggle = document.querySelector('.mobile-sidebar-toggle');
        if (mobileToggle) {
            mobileToggle.addEventListener('click', () => {
                sidebar.classList.toggle('show');
            });
        }

        // Close sidebar on mobile when clicking outside
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 768) {
                if (!sidebar.contains(e.target) && !e.target.classList.contains('mobile-sidebar-toggle')) {
                    sidebar.classList.remove('show');
                }
            }
        });
    }

    initTheme() {
        const themeToggle = document.querySelector('.theme-toggle');
        const currentTheme = localStorage.getItem('adminTheme') || 'light';
        
        document.body.classList.toggle('admin-dark-mode', currentTheme === 'dark');
        
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                document.body.classList.toggle('admin-dark-mode');
                const isDark = document.body.classList.contains('admin-dark-mode');
                localStorage.setItem('adminTheme', isDark ? 'dark' : 'light');
                this.updateThemeIcon(isDark);
            });
        }
        
        this.updateThemeIcon(currentTheme === 'dark');
    }

    updateThemeIcon(isDark) {
        const themeIcon = document.querySelector('.theme-toggle i');
        if (themeIcon) {
            themeIcon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
        }
    }

    initRealTimeUpdates() {
        // Update statistics every 30 seconds
        setInterval(() => {
            this.updateStatistics();
        }, 30000);

        // Update notifications every 10 seconds
        setInterval(() => {
            this.checkNotifications();
        }, 10000);
    }

    bindEvents() {
        // Form submissions
        this.bindFormSubmissions();
        
        // Search and filter
        this.bindSearchAndFilter();
        
        // Bulk actions
        this.bindBulkActions();
        
        // Auto-save
        this.bindAutoSave();
    }

    bindFormSubmissions() {
        // Generic form submission handler
        document.addEventListener('submit', async (e) => {
            if (e.target.classList.contains('admin-form')) {
                e.preventDefault();
                await this.handleFormSubmission(e.target);
            }
        });
    }

    bindSearchAndFilter() {
        // Real-time search
        const searchInputs = document.querySelectorAll('.admin-search');
        searchInputs.forEach(input => {
            input.addEventListener('input', this.debounce((e) => {
                this.performSearch(e.target.value, e.target.dataset.target);
            }, 300));
        });

        // Filter dropdowns
        const filterSelects = document.querySelectorAll('.admin-filter');
        filterSelects.forEach(select => {
            select.addEventListener('change', (e) => {
                this.applyFilter(e.target.value, e.target.dataset.filter);
            });
        });
    }

    bindBulkActions() {
        // Select all checkbox
        const selectAllCheckbox = document.querySelector('.select-all');
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', (e) => {
                const checkboxes = document.querySelectorAll('.item-checkbox');
                checkboxes.forEach(checkbox => {
                    checkbox.checked = e.target.checked;
                });
                this.updateBulkActionButtons();
            });
        }

        // Individual checkboxes
        document.addEventListener('change', (e) => {
            if (e.target.classList.contains('item-checkbox')) {
                this.updateBulkActionButtons();
            }
        });

        // Bulk action buttons
        const bulkActionBtns = document.querySelectorAll('.bulk-action-btn');
        bulkActionBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.target.dataset.action;
                const selectedItems = this.getSelectedItems();
                this.performBulkAction(action, selectedItems);
            });
        });
    }

    bindAutoSave() {
        const autoSaveInputs = document.querySelectorAll('.auto-save');
        autoSaveInputs.forEach(input => {
            input.addEventListener('change', this.debounce((e) => {
                this.autoSave(e.target);
            }, 1000));
        });
    }

    async handleFormSubmission(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        // Show loading state
        submitBtn.innerHTML = '<span class="admin-spinner"></span> Processing...';
        submitBtn.disabled = true;

        try {
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: form.method,
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                this.showNotification('Success!', result.message || 'Operation completed successfully', 'success');
                
                // Reset form if specified
                if (form.dataset.resetOnSuccess === 'true') {
                    form.reset();
                }
                
                // Reload page if specified
                if (form.dataset.reloadOnSuccess === 'true') {
                    setTimeout(() => location.reload(), 1000);
                }
                
                // Close modal if in modal
                const modal = form.closest('.modal');
                if (modal) {
                    bootstrap.Modal.getInstance(modal).hide();
                }
            } else {
                const error = await response.json();
                this.showNotification('Error!', error.message || 'An error occurred', 'error');
            }
        } catch (error) {
            console.error('Form submission error:', error);
            this.showNotification('Error!', 'Network error occurred', 'error');
        } finally {
            // Restore button state
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    }

    performSearch(query, target) {
        const targetElement = document.querySelector(target);
        if (!targetElement) return;

        const rows = targetElement.querySelectorAll('tbody tr');
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            const matches = text.includes(query.toLowerCase());
            row.style.display = matches ? '' : 'none';
        });

        this.updateSearchResults(rows, query);
    }

    applyFilter(value, filterType) {
        const rows = document.querySelectorAll('tbody tr');
        rows.forEach(row => {
            const cell = row.querySelector(`[data-${filterType}]`);
            if (cell) {
                const cellValue = cell.dataset[filterType] || cell.textContent.trim();
                const matches = !value || cellValue === value;
                row.style.display = matches ? '' : 'none';
            }
        });
    }

    updateBulkActionButtons() {
        const selectedItems = this.getSelectedItems();
        const bulkActionContainer = document.querySelector('.bulk-actions');
        
        if (bulkActionContainer) {
            bulkActionContainer.style.display = selectedItems.length > 0 ? 'block' : 'none';
        }
    }

    getSelectedItems() {
        const checkboxes = document.querySelectorAll('.item-checkbox:checked');
        return Array.from(checkboxes).map(checkbox => checkbox.value);
    }

    async performBulkAction(action, items) {
        if (items.length === 0) {
            this.showNotification('Warning!', 'No items selected', 'warning');
            return;
        }

        const confirmed = await this.showConfirmDialog(
            `Are you sure you want to ${action} ${items.length} item(s)?`
        );

        if (!confirmed) return;

        try {
            const response = await fetch('/admin/bulk-action', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: action,
                    items: items
                })
            });

            if (response.ok) {
                this.showNotification('Success!', `${action} completed successfully`, 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                throw new Error('Bulk action failed');
            }
        } catch (error) {
            console.error('Bulk action error:', error);
            this.showNotification('Error!', 'Bulk action failed', 'error');
        }
    }

    async autoSave(input) {
        const value = input.value;
        const key = input.dataset.key;
        
        if (!key) return;

        try {
            const response = await fetch('/admin/auto-save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    key: key,
                    value: value
                })
            });

            if (response.ok) {
                this.showAutoSaveIndicator(input, true);
            } else {
                this.showAutoSaveIndicator(input, false);
            }
        } catch (error) {
            console.error('Auto-save error:', error);
            this.showAutoSaveIndicator(input, false);
        }
    }

    showAutoSaveIndicator(input, success) {
        const indicator = document.createElement('span');
        indicator.className = `auto-save-indicator ${success ? 'success' : 'error'}`;
        indicator.innerHTML = success ? '<i class="fas fa-check"></i>' : '<i class="fas fa-times"></i>';
        
        const existingIndicator = input.parentNode.querySelector('.auto-save-indicator');
        if (existingIndicator) {
            existingIndicator.remove();
        }
        
        input.parentNode.appendChild(indicator);
        
        setTimeout(() => {
            indicator.remove();
        }, 2000);
    }

    async updateStatistics() {
        try {
            const response = await fetch('/admin/api/statistics');
            if (response.ok) {
                const stats = await response.json();
                this.updateStatisticsDisplay(stats);
            }
        } catch (error) {
            console.error('Statistics update error:', error);
        }
    }

    updateStatisticsDisplay(stats) {
        Object.keys(stats).forEach(key => {
            const element = document.querySelector(`[data-stat="${key}"]`);
            if (element) {
                this.animateNumber(element, parseInt(element.textContent), stats[key]);
            }
        });
    }

    animateNumber(element, start, end) {
        const duration = 1000;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = Math.floor(start + (end - start) * progress);
            element.textContent = current.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }

    async checkNotifications() {
        try {
            const response = await fetch('/admin/api/notifications');
            if (response.ok) {
                const data = await response.json();
                if (data.notifications) {
                    this.updateNotificationBadge(data.count || data.notifications.length);
                    this.updateNotificationList(data.notifications);
                }
            } else if (response.status === 401) {
                // User not authenticated, silently ignore
                return;
            }
        } catch (error) {
            // Silently ignore authentication errors to avoid console spam
            if (!error.message.includes('Unexpected token')) {
                console.error('Notifications check error:', error);
            }
        }
    }

    updateNotificationBadge(count) {
        const badge = document.querySelector('.notification-badge');
        if (badge) {
            badge.textContent = count;
            badge.style.display = count > 0 ? 'inline' : 'none';
        }
    }

    updateNotificationList(notifications) {
        const list = document.querySelector('.notification-list');
        if (list) {
            list.innerHTML = notifications.map(notification => `
                <div class="notification-item">
                    <div class="notification-content">
                        <h6>${notification.title}</h6>
                        <p>${notification.message}</p>
                        <small>${notification.time}</small>
                    </div>
                </div>
            `).join('');
        }
    }

    showNotification(title, message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show notification-toast`;
        notification.innerHTML = `
            <strong>${title}</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.notification-container') || document.body;
        container.appendChild(notification);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    async showConfirmDialog(message) {
        return new Promise((resolve) => {
            const modal = document.createElement('div');
            modal.className = 'modal fade';
            modal.innerHTML = `
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Confirm Action</h5>
                        </div>
                        <div class="modal-body">
                            <p>${message}</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-danger confirm-btn">Confirm</button>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            const bsModal = new bootstrap.Modal(modal);
            
            modal.querySelector('.confirm-btn').addEventListener('click', () => {
                resolve(true);
                bsModal.hide();
            });
            
            modal.addEventListener('hidden.bs.modal', () => {
                resolve(false);
                modal.remove();
            });
            
            bsModal.show();
        });
    }

    loadSettings() {
        // Load user preferences
        const preferences = JSON.parse(localStorage.getItem('adminPreferences') || '{}');
        this.applyPreferences(preferences);
    }

    applyPreferences(preferences) {
        // Apply saved preferences
        if (preferences.tablePageSize) {
            const pageSizeSelect = document.querySelector('.page-size-select');
            if (pageSizeSelect) {
                pageSizeSelect.value = preferences.tablePageSize;
            }
        }
        
        if (preferences.defaultView) {
            const viewToggle = document.querySelector(`[data-view="${preferences.defaultView}"]`);
            if (viewToggle) {
                viewToggle.click();
            }
        }
    }

    savePreference(key, value) {
        const preferences = JSON.parse(localStorage.getItem('adminPreferences') || '{}');
        preferences[key] = value;
        localStorage.setItem('adminPreferences', JSON.stringify(preferences));
    }

    // Utility function for debouncing
    debounce(func, wait) {
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

    // Export data functionality
    exportData(format, data, filename) {
        let content, mimeType;
        
        switch (format) {
            case 'csv':
                content = this.convertToCSV(data);
                mimeType = 'text/csv';
                break;
            case 'json':
                content = JSON.stringify(data, null, 2);
                mimeType = 'application/json';
                break;
            default:
                console.error('Unsupported export format:', format);
                return;
        }
        
        const blob = new Blob([content], { type: mimeType });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${filename}.${format}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
    }

    convertToCSV(data) {
        if (!data.length) return '';
        
        const headers = Object.keys(data[0]);
        const csvContent = [
            headers.join(','),
            ...data.map(row => headers.map(header => `"${row[header] || ''}"`).join(','))
        ].join('\n');
        
        return csvContent;
    }
}

// Initialize admin dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.adminDashboard = new AdminDashboard();
});

// Global utility functions
window.AdminUtils = {
    formatNumber: (num) => {
        return new Intl.NumberFormat().format(num);
    },
    
    formatDate: (date) => {
        return new Intl.DateTimeFormat().format(new Date(date));
    },
    
    formatCurrency: (amount) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },
    
    truncateText: (text, length = 50) => {
        return text.length > length ? text.substring(0, length) + '...' : text;
    }
};