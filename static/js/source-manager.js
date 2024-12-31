// Source Management functionality
let selectedSourceId = null;

function initializeSourceManager() {
    // Initialize delete source dialog
    const deleteSourceDialog = new DeleteSourceDialog();
    window.deleteSourceDialog = deleteSourceDialog;

    // Update delete button state when source selection changes
    document.addEventListener('sourceSelected', (event) => {
        const deleteBtn = document.getElementById('deleteSourceBtn');
        if (deleteBtn) {
            deleteBtn.disabled = !event.detail.sourceId;
        }
        selectedSourceId = event.detail.sourceId;
    });

    // Listen for successful source deletion
    document.addEventListener('sourceDeleted', (event) => {
        const deletedSourceId = event.detail.sourceId;
        // Remove the source from the UI
        const sourceElement = document.querySelector(`[data-source-id="${deletedSourceId}"]`);
        if (sourceElement) {
            sourceElement.remove();
        }
        // Reset selection
        selectedSourceId = null;
        // Disable delete button
        const deleteBtn = document.getElementById('deleteSourceBtn');
        if (deleteBtn) {
            deleteBtn.disabled = true;
        }
        // Refresh character list
        refreshCharacterList();
    });
}

function selectSource(element, sourceId) {
    // Remove selection from all sources
    document.querySelectorAll('.source-item').forEach(item => {
        item.classList.remove('selected');
    });
    
    // Add selection to clicked source
    element.classList.add('selected');
    selectedSourceId = sourceId;

    // Enable delete button
    const deleteBtn = document.getElementById('deleteSourceBtn');
    if (deleteBtn) {
        deleteBtn.disabled = false;
    }

    // Dispatch source selected event
    const event = new CustomEvent('sourceSelected', {
        detail: { sourceId }
    });
    document.dispatchEvent(event);
}

function showDeleteSourceDialog() {
    if (!selectedSourceId) {
        showNotification('Please select a source to delete', 'error');
        return;
    }

    // Get source name from the selected element
    const sourceElement = document.querySelector(`[data-source-id="${selectedSourceId}"]`);
    const sourceName = sourceElement ? sourceElement.textContent.trim() : 'selected source';

    // Show the delete confirmation dialog
    window.deleteSourceDialog.show(selectedSourceId, sourceName);
}

function handleSourceDeletion(sourceId) {
    return fetch(`/api/transcripts/${sourceId}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to delete source');
        }
        return response.json();
    })
    .then(data => {
        showNotification('Source deleted successfully', 'success');
        const event = new CustomEvent('sourceDeleted', {
            detail: { sourceId }
        });
        document.dispatchEvent(event);
    })
    .catch(error => {
        console.error('Error deleting source:', error);
        showNotification('Failed to delete source', 'error');
    });
}

// Initialize on document load
document.addEventListener('DOMContentLoaded', initializeSourceManager);