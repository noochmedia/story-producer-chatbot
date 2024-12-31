// Character Management System
class CharacterManager {
    constructor() {
        this.characterList = [];
        this.initialize();
    }

    initialize() {
        // Listen for source deletion events
        document.addEventListener('sourceDeleted', () => this.refreshCharacterList());
        
        // Listen for new source uploads
        document.addEventListener('sourceUploaded', () => this.refreshCharacterList());
    }

    async refreshCharacterList() {
        try {
            const response = await fetch('/api/characters/refresh', {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error('Failed to refresh character list');
            }

            const characters = await response.json();
            this.updateCharacterListUI(characters);
            
            showNotification('Character list refreshed', 'success');
            
            // Dispatch event for other components
            const event = new CustomEvent('charactersUpdated', {
                detail: { characters }
            });
            document.dispatchEvent(event);

        } catch (error) {
            console.error('Error refreshing character list:', error);
            showNotification('Failed to refresh character list', 'error');
        }
    }

    updateCharacterListUI(characters) {
        const characterListElement = document.getElementById('characterList');
        if (!characterListElement) return;

        // Clear current list
        characterListElement.innerHTML = '';

        // Add new characters
        characters.forEach(character => {
            const li = document.createElement('li');
            li.className = 'character-item';
            li.setAttribute('data-character-id', character.id);
            
            li.innerHTML = `
                <span class="character-name" title="${character.full_name || character.name}">
                    ${character.name}
                </span>
                <button class="character-delete" onclick="deleteCharacter('${character.id}')" title="Delete character">
                    ×
                </button>
            `;

            characterListElement.appendChild(li);
        });
    }

    async getCharacterBrief(characterId) {
        try {
            const response = await fetch(`/api/characters/${characterId}/brief`);
            if (!response.ok) {
                throw new Error('Failed to get character brief');
            }
            return await response.json();
        } catch (error) {
            console.error('Error getting character brief:', error);
            showNotification('Failed to get character information', 'error');
            return null;
        }
    }

    async deleteCharacter(characterId) {
        try {
            const response = await fetch(`/api/characters/${characterId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Failed to delete character');
            }

            // Remove from UI
            const characterElement = document.querySelector(`[data-character-id="${characterId}"]`);
            if (characterElement) {
                characterElement.remove();
            }

            showNotification('Character deleted successfully', 'success');

        } catch (error) {
            console.error('Error deleting character:', error);
            showNotification('Failed to delete character', 'error');
        }
    }
}

// Initialize character manager and make it globally available
window.characterManager = new CharacterManager();

// Global functions for character management
function refreshCharacterList() {
    return window.characterManager.refreshCharacterList();
}

function deleteCharacter(characterId) {
    return window.characterManager.deleteCharacter(characterId);
}

function showCharacterBrief(characterId) {
    window.characterManager.getCharacterBrief(characterId)
        .then(brief => {
            if (brief) {
                // TODO: Implement character brief display UI
                console.log('Character brief:', brief);
            }
        });
}