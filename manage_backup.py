import os
import sys
from config import Config
from services.backup import BackupService
from utils.logger import logger

def print_usage():
    print("""
Usage: python manage_backup.py <command> [options]

Commands:
    create      Create a new backup
    list        List all available backups
    restore     Restore a specific backup
    
Examples:
    python manage_backup.py create
    python manage_backup.py list
    python manage_backup.py restore backup_20241229_123456
    """)

def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]
    backup_service = BackupService(
        backup_dir=Config.BACKUP_DIR,
        max_backups=Config.MAX_BACKUPS
    )

    try:
        if command == 'create':
            # Get the project root directory (parent of backup dir)
            source_dir = os.path.dirname(os.path.abspath(__file__))
            success = backup_service.create_backup(source_dir)
            if success:
                print("Backup created successfully!")
            else:
                print("Failed to create backup. Check the logs for details.")

        elif command == 'list':
            backups = backup_service.list_backups()
            if not backups:
                print("No backups found.")
            else:
                print("\nAvailable backups:")
                print("-" * 80)
                for backup in backups:
                    status = backup.get('status', 'unknown')
                    if status == 'success':
                        print(f"Name: {backup['backup_name']}")
                        print(f"Created: {backup['timestamp']}")
                        print(f"Status: {status}")
                        print("-" * 80)

        elif command == 'restore':
            if len(sys.argv) < 3:
                print("Error: Please specify the backup name to restore")
                print_usage()
                return

            backup_name = sys.argv[2]
            source_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Confirm before restoration
            confirm = input(f"This will restore {backup_name} to {source_dir}. Continue? (y/N): ")
            if confirm.lower() != 'y':
                print("Restoration cancelled.")
                return

            success = backup_service.restore_backup(backup_name, source_dir)
            if success:
                print("Backup restored successfully!")
            else:
                print("Failed to restore backup. Check the logs for details.")

        else:
            print(f"Unknown command: {command}")
            print_usage()

    except Exception as e:
        logger.error(f"Error in backup management: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()