#!/usr/bin/env python3

import sys
import subprocess
import os
import tempfile
# PySide6 importları
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QCheckBox, QPushButton, QMessageBox, QDialog, QFormLayout, 
    QSizePolicy, QSpacerItem, QProgressBar
)
from PySide6.QtGui import QPixmap, QIcon, QColor, QPainter, QMovie
from PySide6.QtCore import Qt, QThread, Signal as pyqtSignal, QTimer 

# GNOME uyumluluğu için ortam değişkenleri
os.environ["QT_QPA_PLATFORMTHEME"] = "qt5ct"
os.environ["QT_ASSUME_STDCORE"] = "1"

# Sabitler
APP_NAME = "G-USB Formatter"
APP_VERSION = "2.1.7" 
APP_LICENSE = "GNU GPL v3"
APP_AUTHOR = "@Zeus & @Gemini" 

# Yeni Hakkında Diyalogu için Sabitler
AUTHOR_NAME = "A. Serhat KILIÇOĞLU"
GITHUB_URL = "www.github.com/shampuan"

# MBR'nin kısıtlı olduğu sınır (2 TB - ondalık, 2,000,000,000,000 Byte)
TWO_TB_LIMIT = 2 * 1000**4 

# Dil desteği için sözlükler
TRANSLATIONS = {
    "en": {
        # Temel Çeviriler (Aynı Kaldı)
        "version": "Version",
        "disk": "Disk:",
        "format": "Format:",
        "partition": "Partition:",
        "cluster_size": "Block/Cluster Size:", 
        "label": "Label:",
        "quick_format": "Quick Format (Data recoverable, faster)",
        "format_button": "Format",
        "about_button": "About",
        "no_usb_found": "No USB disk found",
        "warning": "Warning",
        "no_disk_selected": "No disk selected for formatting",
        "confirmation": "Confirmation",
        "confirm_message": "<b>{}</b> disk will be formatted!\nFormat: {} | Partition: {}\nQuick Format: {}\n\nALL DATA WILL BE LOST! Continue?",
        "yes": "Yes",
        "no": "No",
        "already_running": "A process is already running",
        "success": "Success",
        "error": "Error",
        "process_started_general": "Formatting in progress...", 
        "admin_rights": "Requesting admin rights...",
        "format_success": "Format successful!",
        "label_placeholder": "Disk label (optional)",
        "zero_fill_started": "Disk zero-fill started. This may take a long time...",
        "zero_fill_finished": "Disk zero-fill finished.",
        "MSG": "Message",
        "cluster_size_default": "Default",
        "gpt_enforced_tooltip": "MBR does not support disks larger than 2TB. GPT is enforced.", 
        "gpt_info_message": f"This drive is larger than 2TB (or {int(TWO_TB_LIMIT/1000**4)} TB) and requires GPT partitioning. The system automatically enforced GPT for compatibility.",
        "gpt_enforced_message": "The selected disk is larger than 2TB and *must* be partitioned using GPT. The operation is cancelled.",
        
        # Yeni Hakkında Diyalogu Anahtarları (İstek 1 Düzeltmeler)
        "license_label": "License", # Baş harf büyük ve çeviriye dahil
        "program_language": "Programming Language", # İki nokta üst üste kaldırıldı
        "interface": "Interface", # İki nokta üst üste kaldırıldı
        "author": "Author", # İki nokta üst üste kaldırıldı
        "github": "Github", # İki nokta üst üste kaldırıldı
        "description_text": "This program formats your flash drives according to your desired settings. It is open source and licensed under GPLv3.",
        "no_warranty": "THIS PROGRAM COMES WITH ABSOLUTELY NO WARRANTY.",
        "copyright_text": f"Copyright \u00a9 2025 {AUTHOR_NAME}"
    },
    "tr": {
        # Temel Çeviriler (Aynı Kaldı)
        "version": "Sürüm",
        "disk": "Disk:",
        "format": "Biçim:",
        "partition": "Bölümleme:",
        "cluster_size": "Blok/Küme Boyutu:", 
        "label": "Etiket:",
        "quick_format": "Hızlı Biçimlendir (Veri kurtarılabilir, daha hızlıdır)",
        "format_button": "Biçimlendir",
        "about_button": "Hakkında",
        "no_usb_found": "USB disk bulunamadı",
        "warning": "Uyarı",
        "no_disk_selected": "Biçimlendirilecek disk seçilmedi",
        "confirmation": "Onay",
        "confirm_message": "<b>{}</b> diski biçimlendirilecek!\nBiçim: {} | Bölümleme: {}\nHızlı Biçimlendirme: {}\n\nTÜM VERİLER SİLİNECEK! Devam?",
        "yes": "Evet",
        "no": "Hayır",
        "already_running": "Zaten bir işlem çalışıyor",
        "success": "Başarılı",
        "error": "Hata",
        "process_started_general": "Biçimlendirme işlemi sürüyor...", 
        "admin_rights": "Yönetici hakları isteniyor...",
        "format_success": "Biçimlendirme başarılı!",
        "label_placeholder": "Disk etiketi (isteğe bağlı)",
        "zero_fill_started": "Diski sıfırlarla doldurma işlemi başlatıldı. Bu işlem uzun sürebilir...",
        "zero_fill_finished": "Diski sıfırlarla doldurma işlemi tamamlandı.",
        "MSG": "Mesaj",
        "cluster_size_default": "Varsayılan",
        "gpt_enforced_tooltip": "MBR does not support disks larger than 2TB. GPT is enforced.", 
        "gpt_info_message": f"Bu sürücü 2TB'den ({int(TWO_TB_LIMIT/1000**4)} TB) daha büyüktür ve GPT bölümleme gerektirir. Sistem uyumluluk için GPT'yi otomatik olarak zorunlu kıldı.",
        "gpt_enforced_message": "Seçilen disk 2TB'den daha büyüktür ve *kesinlikle* GPT bölümleme kullanılarak biçimlendirilmelidir. İşlem iptal edildi.",

        # Yeni Hakkında Diyalogu Anahtarları (İstek 1 Düzeltmeler)
        "license_label": "Lisans", # Baş harf büyük ve çeviriye dahil
        "program_language": "Programlama Dili", # İki nokta üst üste kaldırıldı
        "interface": "Arayüz", # İki nokta üst üste kaldırıldı
        "author": "Yazar", # İki nokta üst üste kaldırıldı
        "github": "Github", # İki nokta üst üste kaldırıldı
        "description_text": "Bu program, flaşbelleklerinizi istediğiniz ayarlara göre biçimlendirir. Açık kaynak kodludur ve GPLv3 lisansına sahiptir.",
        "no_warranty": "BU PROGRAM KESİNLİKLE GARANTİ GETİRMEZ.",
        "copyright_text": f"Telif Hakkı \u00a9 2025 {AUTHOR_NAME}"
    }
}

# Komut yolları ve desteklenen boyutlar (Aynı kaldı)
COMMAND_PATHS = {
    "lsblk": "/usr/bin/lsblk",
    "mkfs.ntfs": "/usr/sbin/mkfs.ntfs",
    "mkfs.fat": "/usr/sbin/mkfs.fat",
    "mkfs.exfat": "/usr/sbin/mkfs.exfat",
    "mkfs.ext4": "/usr/sbin/mkfs.ext4",
    "parted": "/usr/sbin/parted",
    "umount": "/usr/bin/umount",
    "udevadm": "/usr/bin/udevadm",
    "sfdisk": "/usr/sbin/sfdisk",
    "dd": "/usr/bin/dd"
}

SUPPORTED_BLOCK_SIZES = {
    "NTFS": ["512", "1024", "2048", "4096", "8192", "16384", "32768", "65536"],
    "FAT32": ["512", "1024", "2048", "4096", "8192", "16384", "32768"],
    "ExFAT": ["512", "1024", "2048", "4096", "8192", "16384", "32768", "65536"],
    "Ext4": ["1024", "2048", "4096"]
}


def get_resource_path(relative_path):
    base_path = os.path.abspath(os.path.dirname(__file__))
    current_dir_path = os.path.join(base_path, relative_path)
    if os.path.exists(current_dir_path):
        return current_dir_path

    if hasattr(sys, '_MEIPASS'):
        bundle_dir_path = os.path.join(sys._MEIPASS, relative_path)
        if os.path.exists(bundle_dir_path):
            return bundle_dir_path

    system_icon_path = os.path.join("/usr/share/G-USB-Formatter/icons", relative_path)
    if os.path.exists(system_icon_path):
        return system_icon_path
            
    return relative_path

class BusyDialog(QDialog):
    def __init__(self, parent=None, language="tr"):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle(self.tr("MSG"))
        self.setFixedSize(300, 100) 
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) 
        
        self.language = language

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        label = QLabel(self.tr("process_started_general"))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 14px; margin-bottom: 5px;")

        progress_bar = QProgressBar(self)
        progress_bar.setRange(0, 0)
        progress_bar.setTextVisible(False)

        layout.addWidget(label)
        layout.addWidget(progress_bar)
        
        if parent:
            self.move(parent.geometry().center() - self.rect().center())
        
    def tr(self, key):
        if self.parent() and hasattr(self.parent(), 'tr'):
            return self.parent().tr(key)
        return TRANSLATIONS[self.language].get(key, key)


class DiskOperationThread(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, disk, format_type, cluster_size, label, quick_format, partition_scheme="msdos", language="tr"):
        super().__init__()
        self.disk = disk
        self.format_type = format_type
        self.cluster_size = cluster_size 
        self.label = label
        self.quick_format = quick_format
        self.partition_scheme = partition_scheme
        self.language = language

    def tr(self, key):
        return TRANSLATIONS[self.language].get(key, key)

    def run(self):
        temp_script_path = None
        try:
            # ... (Komutlar ve formatlama mantığı aynı kaldı) ...
            script_content = []
            script_content.append("#!/bin/bash")
            script_content.append("set -e")

            # Bölümleri çıkar
            script_content.append(f"{COMMAND_PATHS.get('lsblk')} -o NAME,MOUNTPOINT -nl -p {self.disk} | awk '$2 != \"\" {{print $1}}' | while read -r part; do")
            script_content.append(f"    {COMMAND_PATHS.get('umount')} \"$part\" || true")
            script_content.append("done")

            # Sıfırlarla doldurma
            if not self.quick_format:
                dd_path = COMMAND_PATHS.get("dd")
                if not dd_path:
                    raise FileNotFoundError(f"dd {self.tr('komutu bulunamadı')}")
                script_content.append(f"echo \"{self.tr('zero_fill_started')} \"")
                script_content.append(f"{dd_path} if=/dev/zero of=\"{self.disk}\" bs=4M status=progress oflag=sync || true") 
                script_content.append(f"echo \"{self.tr('zero_fill_finished')} \"")
            
            # Bölüm tablosu oluştur
            script_content.append(f"echo \"{self.partition_scheme} bölüm tablosu oluşturuluyor...\"")
            script_content.append(f"{COMMAND_PATHS.get('parted')} -s {self.disk} mklabel {self.partition_scheme}")
            
            # Birincil bölüm oluştur
            script_content.append(f"echo \"Birincil bölüm oluşturuluyor...\"")
            script_content.append(f"{COMMAND_PATHS.get('parted')} -s {self.disk} mkpart primary 0% 100%")
            
            # Bölüm türünü format tipine göre ayarla
            script_content.append(f"echo \"Bölüm türü ayarlanıyor...\"")
            if self.partition_scheme == "msdos": 
                if self.format_type == "NTFS":
                    script_content.append(f"echo -e 'type=7' | {COMMAND_PATHS.get('sfdisk')} --label dos {self.disk}")
                elif self.format_type == "FAT32":
                    script_content.append(f"echo -e 'type=c' | {COMMAND_PATHS.get('sfdisk')} --label dos {self.disk}")
                elif self.format_type == "ExFAT":
                    script_content.append(f"echo -e 'type=7' | {COMMAND_PATHS.get('sfdisk')} --label dos {self.disk}")
                elif self.format_type == "Ext4":
                    script_content.append(f"echo -e 'type=83' | {COMMAND_PATHS.get('sfdisk')} --label dos {self.disk}")
            else: 
                if self.format_type == "NTFS":
                    script_content.append(f"{COMMAND_PATHS.get('parted')} -s {self.disk} set 1 msftdata on")
                elif self.format_type == "FAT32":
                    script_content.append(f"{COMMAND_PATHS.get('parted')} -s {self.disk} set 1 esp on")
                elif self.format_type == "ExFAT":
                    script_content.append(f"{COMMAND_PATHS.get('parted')} -s {self.disk} set 1 msftdata on")

            script_content.append(f"{COMMAND_PATHS.get('udevadm')} settle")
            script_content.append("sleep 2")

            # Bölüm adını belirle
            script_content.append("if [[ \"{self.disk}\" == *\"nvme\"* ]]; then")
            script_content.append(f"    PARTITION=\"{self.disk}p1\"")
            script_content.append("else")
            script_content.append(f"    PARTITION=\"{self.disk}1\"")
            script_content.append("fi")
            script_content.append("echo \"Bölüm: $PARTITION\"")

            # Formatlama komutunu oluştur
            mkfs_cmd_name = {
                "NTFS": "mkfs.ntfs",
                "FAT32": "mkfs.fat",
                "ExFAT": "mkfs.exfat",
                "Ext4": "mkfs.ext4"
            }.get(self.format_type)

            if not mkfs_cmd_name:
                raise Exception(self.tr("Geçersiz dosya sistemi seçimi."))
            
            mkfs_path = COMMAND_PATHS.get(mkfs_cmd_name)
            if not mkfs_path:
                raise FileNotFoundError(f"{mkfs_cmd_name} {self.tr('komutu bulunamadı')}")

            mkfs_command = [mkfs_path]

            # Küme boyutu ayarı
            if self.cluster_size != self.tr("cluster_size_default"):
                size_value = self.cluster_size 
                if self.format_type == "NTFS":
                    mkfs_command.extend(['-c', size_value, '--force', '-f']) 
                elif self.format_type == "FAT32":
                    mkfs_command.extend(['-S', size_value])
                elif self.format_type == "ExFAT":
                    mkfs_command.extend(['-c', size_value])
                elif self.format_type == "Ext4":
                    mkfs_command.extend(['-b', size_value]) 
                
                script_content.append(f"echo \"{self.tr('cluster_size_set').format(size_value)}\"")

            # Format tipine göre özelleştirmeler
            if self.format_type == "NTFS":
                if self.quick_format:
                    mkfs_command.append('-Q')
                if self.label:
                    mkfs_command.extend(['-L', self.label])
            elif self.format_type == "FAT32":
                mkfs_command.extend(['-F', '32'])
                if not self.quick_format:
                    mkfs_command.append('-c')
                if self.label:
                    mkfs_command.extend(['-n', self.label[:11]])
            elif self.format_type == "Ext4":
                if not self.quick_format:
                    mkfs_command.append('-c')
                if self.label:
                    mkfs_command.extend(['-L', self.label])
            elif self.format_type == "ExFAT":
                if self.label:
                    mkfs_command.extend(['-L', self.label])

            mkfs_command.append("$PARTITION")
            script_content.append(' '.join(mkfs_command))

            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh', encoding='utf-8') as tmp_file:
                tmp_file.write('\n'.join(script_content))
                temp_script_path = tmp_file.name
            
            os.chmod(temp_script_path, 0o755)
            
            proc = subprocess.Popen(['pkexec', temp_script_path],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)
            
            stdout_lines = []
            stderr_lines = []
            while True:
                line_stdout = proc.stdout.readline()
                line_stderr = proc.stderr.readline()
                if line_stdout:
                    stdout_lines.append(line_stdout.strip())
                if line_stderr:
                    stderr_lines.append(line_stderr.strip())

                if not line_stdout and not line_stderr and proc.poll() is not None:
                    break
            
            proc.wait() 
            
            if proc.returncode != 0:
                error_message = f"{self.tr('İşlem hatası')} (Kod: {proc.returncode})\nStderr: {' '.join(stderr_lines)}"
                raise Exception(error_message)
            
            self.finished.emit(True, self.tr("format_success"))

        except Exception as e:
            self.finished.emit(False, f"{self.tr('error')}: {str(e)}")
        finally:
            if temp_script_path and os.path.exists(temp_script_path):
                try:
                    os.remove(temp_script_path)
                except:
                    pass

class USBFormatterApp(QWidget):
    # Sabit pencere boyutu (Önceki istekten 520 olarak kaldı)
    FIXED_WIDTH = 450
    FIXED_HEIGHT = 520 
    
    def __init__(self):
        super().__init__()
        self.current_language = "tr"
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon(get_resource_path('usb_icon.png')))
        self.setFixedSize(self.FIXED_WIDTH, self.FIXED_HEIGHT) 
        self.thread = None
        self.disk_sizes = {} 
        self.busy_dialog = None 
        
        self.movie = QMovie(get_resource_path('usb_icon.gif'))
        self.usb_icon_label = None
        self.original_pixmap = None
        
        # İstek 2: QLineEdit'ın (Disk Etiketi) yüksekliğini artırmak için CSS güncellemesi
        self.setStyleSheet("QComboBox, QPushButton, QLineEdit { min-height: 30px; }")

        self.init_ui()
        self.load_disks()
        

    def tr(self, key):
        return TRANSLATIONS[self.current_language].get(key, key)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        self.usb_icon_label = QLabel()
        self.usb_icon_label.setAlignment(Qt.AlignCenter)
        self.set_static_icon()
        
        icon_container = QHBoxLayout()
        icon_container.addStretch()
        icon_container.addWidget(self.usb_icon_label)
        icon_container.addStretch()
        
        main_layout.addLayout(icon_container)
        main_layout.addSpacing(10)

        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(10)
        
        # Disk
        self.disk_label = QLabel(self.tr("disk"))
        self.disk_combo = QComboBox()
        self.disk_combo.currentIndexChanged.connect(self.check_disk_size_for_partition_scheme)
        form_layout.addRow(self.disk_label, self.disk_combo)

        # Format
        self.format_label = QLabel(self.tr("format"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["NTFS", "FAT32", "ExFAT", "Ext4"])
        self.format_combo.currentTextChanged.connect(self.update_cluster_size_options) 
        form_layout.addRow(self.format_label, self.format_combo)

        # Partition
        self.partition_label = QLabel(self.tr("partition"))
        self.partition_combo = QComboBox()
        self.partition_combo.addItems(["MBR", "GPT"])
        form_layout.addRow(self.partition_label, self.partition_combo)

        # Blok/Küme Boyutu
        self.cluster_size_label = QLabel(self.tr("cluster_size"))
        self.cluster_size_combo = QComboBox()
        self.update_cluster_size_options() 
        form_layout.addRow(self.cluster_size_label, self.cluster_size_combo)
        
        # Etiket (QLineEdit)
        self.label_label = QLabel(self.tr("label"))
        self.label_input = QLineEdit()
        # min-height: 30px ayarı CSS ile yapıldı
        self.label_input.setPlaceholderText(self.tr("label_placeholder"))
        form_layout.addRow(self.label_label, self.label_input)
        
        main_layout.addLayout(form_layout)

        self.quick_format_check = QCheckBox(self.tr("quick_format"))
        self.quick_format_check.setChecked(True)
        main_layout.addWidget(self.quick_format_check)

        # Düğmeler
        button_layout = QHBoxLayout()
        
        self.format_button = QPushButton(self.tr("format_button"))
        self.format_button.clicked.connect(self.start_format_process)
        button_layout.addWidget(self.format_button)

        self.language_button = QPushButton("Language") 
        self.language_button.clicked.connect(self.toggle_language)
        button_layout.addWidget(self.language_button)

        main_layout.addLayout(button_layout)

        self.about_button = QPushButton(self.tr("about_button"))
        self.about_button.clicked.connect(self.show_about_dialog)
        main_layout.addWidget(self.about_button)
        
        self.setLayout(main_layout)
        
    def parse_size(self, size_str):
        if not size_str:
            return 0
        
        size_str = size_str.upper()
        numeric_part = size_str[:-1].replace(',', '.') 

        try:
            if size_str.endswith('T'):
                return float(numeric_part) * 1000**4 
            elif size_str.endswith('G'):
                return float(numeric_part) * 1000**3 
            elif size_str.endswith('M'):
                return float(numeric_part) * 1000**2 
        except ValueError:
            return 0 
        
        return 0

    def load_disks(self):
        self.disk_combo.clear()
        self.disk_sizes = {} 
        try:
            result = subprocess.run(
                [COMMAND_PATHS['lsblk'], '-o', 'NAME,RM,TYPE,SIZE,MODEL', '-nl', '-p'],
                capture_output=True, text=True)
            
            disks = []
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 4 and parts[2] == 'disk' and parts[1] == '1':
                    disk_path = parts[0]
                    disk_size_str = parts[3] 
                    disk_size_bytes = self.parse_size(disk_size_str)
                    
                    self.disk_sizes[disk_path] = disk_size_bytes
                    
                    disk_info = f"{disk_path} ({disk_size_str})"
                    if len(parts) > 4:
                        disk_info += f" [{' '.join(parts[4:])}]"
                    disks.append(disk_info)
            
            if disks:
                self.disk_combo.addItems(disks)
                self.check_disk_size_for_partition_scheme()
            else:
                self.disk_combo.addItem(self.tr("no_usb_found"))
                
        except Exception as e:
            QMessageBox.critical(self, self.tr("error"), f"{self.tr('error')}: {str(e)}")
            
    def check_disk_size_for_partition_scheme(self):
        """2TB üzerindeki diskler için GPT zorunluluğunu uygular."""
        selected_disk_text = self.disk_combo.currentText()
        if not selected_disk_text or self.tr("no_usb_found") in selected_disk_text:
            self.partition_combo.setEnabled(True)
            self.partition_combo.setToolTip("")
            return

        disk_path = selected_disk_text.split()[0]
        disk_size_bytes = self.disk_sizes.get(disk_path, 0)
        
        if disk_size_bytes > TWO_TB_LIMIT:
            self.partition_combo.setCurrentText("GPT")
            self.partition_combo.setEnabled(False)
            self.partition_combo.setToolTip(self.tr("gpt_enforced_tooltip")) 
        else:
            self.partition_combo.setEnabled(True)
            self.partition_combo.setToolTip("")
            
    def update_cluster_size_options(self):
        """Blok/Küme boyutu seçeneklerini günceller"""
        current_format = self.format_combo.currentText()
        self.cluster_size_combo.clear()
        self.cluster_size_combo.addItem(self.tr("cluster_size_default"))
        self.cluster_size_combo.addItems(SUPPORTED_BLOCK_SIZES.get(current_format, []))

    def toggle_language(self):
        """Dil değiştirme fonksiyonu"""
        self.current_language = "en" if self.current_language == "tr" else "tr"
        self.update_ui_language()

    def update_ui_language(self):
        """Arayüz dilini günceller"""
        self.setWindowTitle(APP_NAME)
        
        # Form etiketlerini güncelle
        self.disk_label.setText(self.tr("disk"))
        self.format_label.setText(self.tr("format"))
        self.partition_label.setText(self.tr("partition"))
        self.cluster_size_label.setText(self.tr("cluster_size"))
        self.label_label.setText(self.tr("label"))
        
        # Diğer arayüz elemanlarını güncelle
        self.quick_format_check.setText(self.tr("quick_format"))
        self.format_button.setText(self.tr("format_button"))
        self.about_button.setText(self.tr("about_button"))
        self.label_input.setPlaceholderText(self.tr("label_placeholder"))
        
        self.update_cluster_size_options()
        
        self.load_disks() 

    def set_static_icon(self):
        if hasattr(self, 'movie') and self.movie:
            self.movie.stop()
        
        pixmap = QPixmap(get_resource_path('usb_icon.png'))
        if pixmap.isNull():
            pixmap = QPixmap(100, 100)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QColor(102, 51, 153))
            painter.drawEllipse(0, 0, 100, 100)
            painter.end()
        
        self.original_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.usb_icon_label.setPixmap(self.original_pixmap)
        self.usb_icon_label.setFixedSize(100, 100)

    def set_animated_icon(self):
        gif_path = get_resource_path('usb_icon.gif')
        if os.path.exists(gif_path):
            self.movie = QMovie(gif_path)
            
            self.movie.setScaledSize(self.original_pixmap.size())
            self.usb_icon_label.setMovie(self.movie)
            self.usb_icon_label.setFixedSize(self.original_pixmap.size())
            
            if self.movie.isValid():
                self.movie.start()
        else:
            self.set_static_icon()

    def show_about_dialog(self):
        # İstek 1: Hakkında menüsü düzeltmeleri
        
        # Zengin metin (HTML) içeriği oluşturuluyor
        html_content = f"""
        <html>
        <head>
            <style>
                h3 {{ margin-bottom: 5px; }}
                .details {{ margin-left: 20px; font-size: 11px; }}
                .warning {{ color: red; font-weight: bold; margin-top: 15px; }}
                /* info-label içindeki iki nokta üst üste HTML içinde eklendi */
                .info-label {{ font-weight: bold; width: 150px; display: inline-block; }} 
            </style>
        </head>
        <body>
            <h3>G-USB Formatter {self.tr('about_button')}</h3>
            <p class="details">
                <span class="info-label">{self.tr('version')}:</span> {APP_VERSION}<br>
                <span class="info-label">{self.tr('license_label')}:</span> {APP_LICENSE}<br>
                <span class="info-label">{self.tr('program_language')}:</span> Python3<br>
                <span class="info-label">{self.tr('interface')}:</span> PySide-6<br>
                <span class="info-label">{self.tr('author')}:</span> {AUTHOR_NAME}<br>
                <span class="info-label">{self.tr('github')}:</span> <a href="http://{GITHUB_URL}">{GITHUB_URL}</a>
            </p>
            <p>{self.tr('description_text')}</p>
            <p class="warning">{self.tr('no_warranty')}</p>
            <hr>
            <p style="font-size: 10px;">{self.tr('copyright_text')}</p>
        </body>
        </html>
        """
        
        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle(self.tr("about_button"))
        about_dialog.setTextFormat(Qt.RichText)
        about_dialog.setText(html_content)
        
        icon_path = get_resource_path('usb_icon.png')
        if os.path.exists(icon_path):
            about_dialog.setIconPixmap(QPixmap(icon_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            about_dialog.setIcon(QMessageBox.Information)

        about_dialog.setStandardButtons(QMessageBox.Ok)
        
        about_dialog.exec_()
    
    def start_format_process(self):
        selected_disk_text = self.disk_combo.currentText()
        if not selected_disk_text or self.tr("no_usb_found") in selected_disk_text:
            QMessageBox.warning(self, self.tr("warning"), self.tr("no_disk_selected"))
            return

        disk_path = selected_disk_text.split()[0]
        format_type = self.format_combo.currentText()
        partition_scheme = "msdos" if "MBR" in self.partition_combo.currentText() else "gpt"
        quick_format = self.quick_format_check.isChecked()
        cluster_size = self.cluster_size_combo.currentText() 
        
        disk_size_bytes = self.disk_sizes.get(disk_path, 0)
        
        if disk_size_bytes > TWO_TB_LIMIT:
            if partition_scheme == "msdos":
                QMessageBox.critical(self, self.tr("error"), self.tr("gpt_enforced_message"))
                return
            
            required_info_msg = QMessageBox(self)
            required_info_msg.setWindowTitle(self.tr("warning"))
            required_info_msg.setText(self.tr("gpt_info_message"))
            required_info_msg.setIcon(QMessageBox.Information)
            required_info_msg.setStandardButtons(QMessageBox.Ok)
            required_info_msg.exec_()

        reply = QMessageBox.warning(
            self, self.tr("confirmation"),
            self.tr("confirm_message").format(
                disk_path, 
                format_type, 
                partition_scheme,
                self.tr("yes") if quick_format else self.tr("no")
            ),
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.start_format_thread(
                disk=disk_path,
                format_type=format_type,
                cluster_size=cluster_size, 
                label=self.label_input.text().strip(),
                quick_format=quick_format,
                partition_scheme=partition_scheme
            )

    def start_format_thread(self, disk, format_type, cluster_size, label, quick_format, partition_scheme):
        if self.thread and self.thread.isRunning():
            QMessageBox.warning(self, self.tr("warning"), self.tr("already_running"))
            return

        self.format_button.setEnabled(False)
        self.set_animated_icon()
        
        self.busy_dialog = BusyDialog(self, self.current_language)
        
        def start_delayed_thread():
            self.busy_dialog.show()
            QApplication.processEvents() 
            
            self.thread = DiskOperationThread(
                disk=disk,
                format_type=format_type,
                cluster_size=cluster_size, 
                label=label,
                quick_format=quick_format,
                partition_scheme=partition_scheme,
                language=self.current_language
            )
            self.thread.finished.connect(self.format_finished)
            self.thread.start()

        QTimer.singleShot(300, start_delayed_thread)


    def format_finished(self, success, message):
        self.format_button.setEnabled(True)
        self.set_static_icon()
        
        if self.busy_dialog:
            self.busy_dialog.close()
            self.busy_dialog = None
        
        if success:
            QMessageBox.information(self, self.tr("success"), message)
            self.load_disks()
        else:
            QMessageBox.critical(self, self.tr("error"), message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = USBFormatterApp()
    ex.show()
    sys.exit(app.exec())
