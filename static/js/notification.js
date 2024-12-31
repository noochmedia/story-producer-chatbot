// Notification System
class NotificationSystem {
    constructor() {
        this.notificationQueue = [];
        this.isShowingNotification = false;
        this.initialize();
    }

    initialize() {
        // Create notification container if it doesn't exist
        if (!document.querySelector('.notification-container')) {
            const container = document.createElement('div');
            container.className = 'notification-container';
            document.body.appendChild(container);
        }
    }

    createNotificationElement(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        
        notification.innerHTML = `
            <span class="notification-message">${message}</span>
            <button class="notification-close" aria-label="Close notification">×</button>
        `;

        const closeButton = notification.querySelector('.notification-close');
        closeButton.addEventListener('click', () => this.hideNotification(notification));

        return notification;
    }

    showNotification(message, type = 'success') {
        const notification = this.createNotificationElement(message, type);
        
        // Add to queue if already showing a notification
        if (this.isShowingNotification) {
            this.notificationQueue.push({ notification, message, type });
            return;
        }

        this.displayNotification(notification);
    }

    displayNotification(notification) {
        this.isShowingNotification = true;
        const container = document.querySelector('.notification-container');
        container.appendChild(notification);
        notification.style.display = 'block';

        // Auto-hide after 3 seconds
        setTimeout(() => {
            this.hideNotification(notification);
        }, 3000);
    }

    hideNotification(notification) {
        notification.style.animation = 'slideOut 0.3s ease-out';
        
        notification.addEventListener('animationend', () => {
            notification.remove();
            this.isShowingNotification = false;
            
            // Show next notification in queue if any
            if (this.notificationQueue.length > 0) {
                const next = this.notificationQueue.shift();
                this.displayNotification(next.notification);
            }
        }, { once: true });
    }
}

// Initialize notification system and make it globally available
window.notificationSystem = new NotificationSystem();

// Global function to show notifications
function showNotification(message, type = 'success') {
    window.notificationSystem.showNotification(message, type);
}