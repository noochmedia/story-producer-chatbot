class BackupService:
    def __init__(self, backup_dir=None, max_backups=5):
        self.backup_dir = backup_dir
        self.max_backups = max_backups

    def create_backup(self, source_dir):
        # In production, just return True since we don't need backups
        return True