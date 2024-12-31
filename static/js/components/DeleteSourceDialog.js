class DeleteSourceDialog {
    constructor() {
        this.dialog = null;
        this.initialize();
    }

    initialize() {
        // Create dialog HTML
        const dialogHTML = `
            <div class="delete-source-dialog modal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Delete Source</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p>Are you sure you want to delete <span class="source-name"></span>?</p>
                            <div class="alert alert-warning">
                                <i class="fas fa-exclamation-triangle"></i>
                                <span>This will update the character list and remove characters that only appear in this source.</span>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-danger confirm-delete">Delete</button>
                        </div>
                    </div>
                </div>
            </div>`;

        // Add dialog to document
        document.body.insertAdjacentHTML('beforeend', dialogHTML);
        this.dialog = document.querySelector('.delete-source-dialog');
        
        // Initialize event listeners
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        const confirmButton = this.dialog.querySelector('.confirm-delete');
        confirmButton.addEventListener('click', () => {
            if (this.currentSourceId) {
                this.deleteSource(this.currentSourceId);
            }
        });
    }

    show(sourceId, sourceName) {
        this.currentSourceId = sourceId;
        const sourceNameSpan = this.dialog.querySelector('.source-name');
        sourceNameSpan.textContent = sourceName;
        
        // Show dialog using Bootstrap modal
        const modal = new bootstrap.Modal(this.dialog);
        modal.show();
    }

    async deleteSource(sourceId) {
        try {
            const response = await fetch(`/api/transcripts/${sourceId}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error('Failed to delete source');
            }

            // Hide dialog
            const modal = bootstrap.Modal.getInstance(this.dialog);
            modal.hide();

            // Emit custom event for successful deletion
            const event = new CustomEvent('sourceDeleted', {
                detail: { sourceId }
            });
            document.dispatchEvent(event);

            // Show success notification
            showNotification('Source deleted successfully', 'success');

            // Refresh character list
            await refreshCharacterList();

        } catch (error) {
            console.error('Error deleting source:', error);
            showNotification('Failed to delete source', 'error');
        }
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    window.deleteSourceDialog = new DeleteSourceDialog();
});