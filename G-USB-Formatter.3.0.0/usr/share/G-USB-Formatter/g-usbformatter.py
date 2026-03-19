#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import os
import tempfile
# PyQt6 importları - PySide6 tamamen kaldırıldı
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QCheckBox, QPushButton, QMessageBox, QDialog, QFormLayout, 
    QProgressBar
)
from PyQt6.QtGui import QPixmap, QIcon, QColor, QPainter, QMovie
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer 

# Wayland ve modern masaüstü ortamları için uyumluluk ayarları
if "GNOME" in os.environ.get("XDG_CURRENT_DESKTOP", ""):
    os.environ["QT_QPA_PLATFORM"] = "wayland;xcb"

# Sabitler
APP_NAME = "G-USB Formatter 3.0"
APP_VERSION = "3.0.0" 
APP_LICENSE = "GNU GPL v3"
APP_AUTHOR = "@shampuan" 

# Yeni Hakkında Diyalogu için Sabitler
AUTHOR_NAME = "A. Serhat KILIÇOĞLU"
GITHUB_URL = "www.github.com/shampuan"

# MBR'nin kısıtlı olduğu sınır (2 TB)
TWO_TB_LIMIT = 2 * 1000**4 

# Dil desteği sözlükleri
TRANSLATIONS = {
    "en": {
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
        "pkg_missing_error": "Error: {} system not found. Please install the required package using 'sudo apt install {}'.",
        "hfs_support": "Apple HFS+ support",
        "btrfs_support": "Btrfs support",
        "xfs_support": "XFS support",
        "process_started_general": "Formatting in progress...", 
        "admin_rights": "Requesting admin rights...",
        "format_success": "Format successful!",
        "label_placeholder": "Disk label (optional)",
        "zero_fill_started": "Disk zero-fill started. This may take a long time...",
        "zero_fill_finished": "Disk zero-fill finished.",
        "MSG": "Message",
        "cluster_size_default": "Default",
        "gpt_enforced_tooltip": "MBR does not support disks larger than 2TB. GPT is enforced.", 
        "gpt_info_message": "This drive is larger than 2TB and requires GPT partitioning. The system automatically enforced GPT for compatibility.",
        "gpt_enforced_message": "The selected disk is larger than 2TB and *must* be partitioned using GPT. The operation is cancelled.",
        "license_label": "License",
        "program_language": "Programming Language",
        "interface": "Interface",
        "author": "Author",
        "github": "Github",
        "description_text": "This program formats your flash drives according to your desired settings. It is open source and licensed under GPLv3.",
        "no_warranty": "THIS PROGRAM COMES WITH ABSOLUTELY NO WARRANTY.",
        "copyright_text": f"Copyright \u00a9 2026 {AUTHOR_NAME}"
    },
    "tr": {
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
        "pkg_missing_error": "Hata: {} sistemi bulunamadı. Lütfen 'sudo apt install {}' komutu ile gerekli paketi yükleyin.",
        "hfs_support": "Apple HFS+ desteği",
        "btrfs_support": "Btrfs desteği",
        "xfs_support": "XFS desteği",
        "process_started_general": "Biçimlendirme işlemi sürüyor...", 
        "admin_rights": "Yönetici hakları isteniyor...",
        "format_success": "Biçimlendirme başarılı!",
        "label_placeholder": "Disk etiketi (isteğe bağlı)",
        "zero_fill_started": "Diski sıfırlarla doldurma işlemi başlatıldı. Bu işlem uzun sürebilir...",
        "zero_fill_finished": "Diski sıfırlarla doldurma işlemi tamamlandı.",
        "MSG": "Mesaj",
        "cluster_size_default": "Varsayılan",
        "gpt_enforced_tooltip": "MBR 2TB'den büyük diskleri desteklemez. GPT zorunludur.", 
        "gpt_info_message": "Bu sürücü 2TB'den daha büyüktür ve GPT bölümleme gerektirir. Sistem uyumluluk için GPT'yi otomatik olarak zorunlu kıldı.",
        "gpt_enforced_message": "Seçilen disk 2TB'den daha büyüktür ve *kesinlikle* GPT bölümleme kullanılarak biçimlendirilmelidir. İşlem iptal edildi.",
        "license_label": "Lisans",
        "program_language": "Programlama Dili",
        "interface": "Arayüz",
        "author": "Yazar",
        "github": "Github",
        "description_text": "Bu program, flaşbelleklerinizi istediğiniz ayarlara göre biçimlendirir. Açık kaynak kodludur ve GPLv3 lisansına sahiptir.",
        "no_warranty": "BU PROGRAM KESİNLİKLE GARANTİ GETİRMEZ.",
        "copyright_text": f"Telif Hakkı \u00a9 2026 {AUTHOR_NAME}"
    }
}

COMMAND_PATHS = {
    "lsblk": "/usr/bin/lsblk",
    "mkfs.ntfs": "/usr/sbin/mkfs.ntfs",
    "mkfs.fat": "/usr/sbin/mkfs.fat",
    "mkfs.exfat": "/usr/sbin/mkfs.exfat",
    "mkfs.ext4": "/usr/sbin/mkfs.ext4",
    "mkfs.btrfs": "/usr/sbin/mkfs.btrfs",
    "mkfs.xfs": "/usr/sbin/mkfs.xfs",
    "mkfs.hfsplus": "/usr/sbin/mkfs.hfsplus",
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
    "Ext4": ["1024", "2048", "4096"],
    "Btrfs": ["4096"],
    "XFS": ["4096"],
    "HFS+": ["4096"]
}

def get_resource_path(relative_path):
    base_path = os.path.abspath(os.path.dirname(__file__))
    # Önce dosyanın tam yanına, sonra yanındaki icons klasörüne bakar
    possible_paths = [
        os.path.join(base_path, relative_path),
        os.path.join(base_path, "icons", relative_path)
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return relative_path

class BusyDialog(QDialog):
    def __init__(self, parent=None, language="tr"):
        super().__init__(parent)
        self.setModal(True)
        self.language = language
        self.setWindowTitle(self.tr("MSG"))
        self.setFixedSize(300, 100) 
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint) 

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        label = QLabel(self.tr("process_started_general"))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 14px; margin-bottom: 5px;")

        progress_bar = QProgressBar(self)
        progress_bar.setRange(0, 0)
        progress_bar.setTextVisible(False)

        layout.addWidget(label)
        layout.addWidget(progress_bar)
        
    def tr(self, key):
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
            script_content = ["#!/bin/bash", "set -e"]
            # Ortam değişkenlerini PKEXEC altına taşıyoruz
            script_content.append("export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin")
            
            script_content.append(f"{COMMAND_PATHS.get('lsblk')} -o NAME,MOUNTPOINT -nl -p {self.disk} | awk '$2 != \"\" {{print $1}}' | while read -r part; do")
            script_content.append(f"    {COMMAND_PATHS.get('umount')} \"$part\" || true")
            script_content.append("done")

            if not self.quick_format:
                script_content.append(f"{COMMAND_PATHS.get('dd')} if=/dev/zero of=\"{self.disk}\" bs=4M status=progress oflag=sync || true")
            
            scheme = "msdos" if self.partition_scheme.lower() == "mbr" else "gpt"
            script_content.append(f"{COMMAND_PATHS.get('parted')} -s {self.disk} mklabel {scheme}")
            script_content.append(f"{COMMAND_PATHS.get('parted')} -s {self.disk} mkpart primary 0% 100%")
            
            if scheme == "msdos": 
                ptype = '7' if self.format_type in ["NTFS", "ExFAT"] else ('c' if self.format_type == "FAT32" else '83')
                script_content.append(f"echo -e 'type={ptype}' | {COMMAND_PATHS.get('sfdisk')} --label dos {self.disk}")
            else: 
                flag = 'msftdata' if self.format_type != "FAT32" else 'esp'
                script_content.append(f"{COMMAND_PATHS.get('parted')} -s {self.disk} set 1 {flag} on")

            script_content.append(f"{COMMAND_PATHS.get('udevadm')} settle\nsleep 2")
            script_content.append(f"if [[ \"{self.disk}\" == *\"nvme\"* || \"{self.disk}\" == *\"mmcblk\"* ]]; then PARTITION=\"{self.disk}p1\"; else PARTITION=\"{self.disk}1\"; fi")

            mkfs_cmd_name = {
                "NTFS": "mkfs.ntfs", 
                "FAT32": "mkfs.fat", 
                "ExFAT": "mkfs.exfat", 
                "Ext4": "mkfs.ext4",
                "Btrfs": "mkfs.btrfs",
                "XFS": "mkfs.xfs",
                "HFS+": "mkfs.hfsplus"
            }.get(self.format_type)
            mkfs_path = COMMAND_PATHS.get(mkfs_cmd_name)
            if not os.path.exists(mkfs_path):
                pkg_map = {"mkfs.hfsplus": "hfsprogs", "mkfs.btrfs": "btrfs-progs", "mkfs.xfs": "xfsprogs"}
                needed_pkg = pkg_map.get(mkfs_cmd_name, "relevant package")
                raise Exception(self.tr("pkg_missing_error").format(mkfs_cmd_name, needed_pkg))
            cmd = [mkfs_path]

            if self.cluster_size != self.tr("cluster_size_default"):
                opt = {
                    'NTFS': '-c', 'FAT32': '-S', 'ExFAT': '-c', 
                    'Ext4': '-b', 'Btrfs': '-s', 'XFS': '-b', 'HFS+': '-b'
                }.get(self.format_type)
                cmd.extend([opt, self.cluster_size])

            if self.format_type == "NTFS":
                if self.quick_format: cmd.append('-Q')
                if self.label: cmd.extend(['-L', self.label])
            elif self.format_type == "FAT32":
                cmd.extend(['-F', '32'])
                if self.label: cmd.extend(['-n', self.label[:11]])
            elif self.format_type in ["Ext4", "ExFAT"]:
                if self.label: cmd.extend(['-L', self.label])
            elif self.format_type == "Btrfs":
                cmd.append('-f')  # Mevcut imzaları zorla geçersiz kıl
                if self.label: cmd.extend(['-L', self.label])
            elif self.format_type == "XFS":
                cmd.append('-f')  # XFS için force parametresi (Resimdeki hatayı çözer)
                if self.label: cmd.extend(['-L', self.label])
            elif self.format_type == "HFS+":
                # HFS+ (mkfs.hfsplus) varsayılan olarak üzerine yazar ancak 
                # tutarlılık için etiketini ekliyoruz.
                if self.label: cmd.extend(['-v', self.label])

            cmd.append("$PARTITION")
            script_content.append(' '.join(cmd))

            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh', encoding='utf-8') as tmp:
                tmp.write('\n'.join(script_content))
                temp_script_path = tmp.name
            
            os.chmod(temp_script_path, 0o755)
            # pkexec'i /bin/bash üzerinden çağırarak yetki ve PATH sorunlarını aşıyoruz
            proc = subprocess.Popen(['pkexec', '/bin/bash', temp_script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = proc.communicate()
            
            if proc.returncode != 0:
                raise Exception(f"{self.tr('error')} (Kod: {proc.returncode})\nDetay: {stderr}")
            
            self.finished.emit(True, self.tr("format_success"))
        except Exception as e:
            self.finished.emit(False, str(e))
        finally:
            if temp_script_path and os.path.exists(temp_script_path):
                try: os.remove(temp_script_path)
                except: pass

class USBFormatterApp(QWidget):
    FIXED_WIDTH = 450
    FIXED_HEIGHT = 520 
    
    def __init__(self):
        super().__init__()
        QApplication.setStyle("Fusion")
        self.current_language = "en"
        self.disk_sizes = {}
        self.thread = None
        self.busy_dialog = None
        self.movie = None
        self.hdd_icon_label = None
        self.flash_icon_label = None
        
        self.init_ui()
        self.load_disks()
        
        self.setFixedSize(self.FIXED_WIDTH, self.FIXED_HEIGHT)
        self.setWindowTitle(APP_NAME)
        icon_path = get_resource_path('usb_icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def tr(self, key):
        return TRANSLATIONS[self.current_language].get(key, key)

    def init_ui(self):
        self.setStyleSheet("QComboBox, QPushButton, QLineEdit { min-height: 30px; }")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        self.usb_icon_label = QLabel()
        # İkonlar için etiketleri oluştur
        self.hdd_icon_label = QLabel()
        self.usb_icon_label = QLabel()
        self.flash_icon_label = QLabel()
        
        # Hizalamaları yap
        self.hdd_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.usb_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flash_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # İkonları yükle
        self.set_static_icon()
        
        # İkonları yan yana dizecek yatay layout
        icon_container = QHBoxLayout()
        icon_container.setSpacing(20) # İkonlar arası boşluk
        icon_container.addStretch()  # Sol boşluk
        icon_container.addWidget(self.hdd_icon_label)
        icon_container.addWidget(self.usb_icon_label)  # Ortada kalacak
        icon_container.addWidget(self.flash_icon_label)
        icon_container.addStretch()  # Sağ boşluk
        
        main_layout.addLayout(icon_container)

        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(10)
        
        self.disk_label = QLabel(self.tr("disk"))
        self.disk_combo = QComboBox()
        self.disk_combo.currentIndexChanged.connect(self.check_disk_size_for_partition_scheme)
        form_layout.addRow(self.disk_label, self.disk_combo)

        self.format_label = QLabel(self.tr("format"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["NTFS", "FAT32", "ExFAT", "Ext4", "Btrfs", "XFS", "HFS+"])
        self.format_combo.currentTextChanged.connect(self.update_cluster_size_options) 
        form_layout.addRow(self.format_label, self.format_combo)

        self.partition_label = QLabel(self.tr("partition"))
        self.partition_combo = QComboBox()
        self.partition_combo.addItems(["MBR", "GPT"])
        form_layout.addRow(self.partition_label, self.partition_combo)

        self.cluster_size_label = QLabel(self.tr("cluster_size"))
        self.cluster_size_combo = QComboBox()
        form_layout.addRow(self.cluster_size_label, self.cluster_size_combo)
        
        self.label_label = QLabel(self.tr("label"))
        self.label_input = QLineEdit()
        self.label_input.setPlaceholderText(self.tr("label_placeholder"))
        form_layout.addRow(self.label_label, self.label_input)
        
        main_layout.addLayout(form_layout)

        self.quick_format_check = QCheckBox(self.tr("quick_format"))
        self.quick_format_check.setChecked(True)
        main_layout.addWidget(self.quick_format_check)

        button_layout = QHBoxLayout()
        self.format_button = QPushButton(self.tr("format_button"))
        self.format_button.clicked.connect(self.start_format_process)
        button_layout.addWidget(self.format_button)

        self.language_button = QPushButton("TR / EN") 
        self.language_button.clicked.connect(self.toggle_language)
        button_layout.addWidget(self.language_button)
        main_layout.addLayout(button_layout)

        self.about_button = QPushButton(self.tr("about_button"))
        self.about_button.clicked.connect(self.show_about_dialog)
        main_layout.addWidget(self.about_button)
        
        self.update_cluster_size_options()

    def parse_size(self, size_str):
        try:
            s = size_str.upper().replace(',', '.')
            val = float(''.join([c for c in s if c.isdigit() or c == '.']))
            if 'T' in s: return val * 1000**4
            if 'G' in s: return val * 1000**3
            if 'M' in s: return val * 1000**2
            return val
        except: return 0

    def load_disks(self):
        self.disk_combo.clear()
        self.disk_sizes = {}
        try:
            res = subprocess.run([COMMAND_PATHS['lsblk'], '-o', 'NAME,RM,TYPE,SIZE,MODEL', '-nl', '-p'], capture_output=True, text=True)
            for line in res.stdout.splitlines():
                p = line.split()
                if len(p) >= 4 and p[2] == 'disk' and p[1] == '1':
                    self.disk_sizes[p[0]] = self.parse_size(p[3])
                    self.disk_combo.addItem(f"{p[0]} ({p[3]}) {' '.join(p[4:]) if len(p) > 4 else ''}")
            if self.disk_combo.count() == 0: self.disk_combo.addItem(self.tr("no_usb_found"))
        except: pass

    def check_disk_size_for_partition_scheme(self):
        txt = self.disk_combo.currentText()
        if not txt or "(" not in txt: return
        path = txt.split()[0]
        if self.disk_sizes.get(path, 0) > TWO_TB_LIMIT:
            self.partition_combo.setCurrentText("GPT")
            self.partition_combo.setEnabled(False)
            QMessageBox.information(self, self.tr("warning"), self.tr("gpt_info_message"))
        else:
            self.partition_combo.setEnabled(True)

    def update_cluster_size_options(self):
        fmt = self.format_combo.currentText()
        self.cluster_size_combo.clear()
        self.cluster_size_combo.addItem(self.tr("cluster_size_default"))
        self.cluster_size_combo.addItems(SUPPORTED_BLOCK_SIZES.get(fmt, []))

    def set_static_icon(self):
        if self.movie: self.movie.stop()
        
        icon_size = 100
        
        def load_pix(name):
            path = get_resource_path(name)
            pix = QPixmap(path)
            if pix.isNull():
                # Dosya bulunamazsa mor daire çiz
                pix = QPixmap(icon_size, icon_size)
                pix.fill(Qt.GlobalColor.transparent)
                p = QPainter(pix)
                p.setBrush(QColor(102, 51, 153))
                p.drawEllipse(0, 0, icon_size, icon_size)
                p.end()
            return pix.scaled(icon_size, icon_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # Ortadaki USB ikonu (png)
        self.usb_icon_label.setFixedSize(icon_size, icon_size)
        self.usb_icon_label.setPixmap(load_pix('usb_icon.png'))

        # Sol taraftaki HDD amblemi
        if self.hdd_icon_label:
            self.hdd_icon_label.setFixedSize(icon_size, icon_size)
            self.hdd_icon_label.setPixmap(load_pix('hddamblem.png'))

        # Sağ taraftaki Flash amblemi
        if self.flash_icon_label:
            self.flash_icon_label.setFixedSize(icon_size, icon_size)
            self.flash_icon_label.setPixmap(load_pix('flashamblem.png'))

    def set_animated_icon(self):
        gif_path = get_resource_path('usb_icon.gif')
        if os.path.exists(gif_path):
            self.movie = QMovie(gif_path)
            self.movie.setScaledSize(self.usb_icon_label.size())
            self.usb_icon_label.setMovie(self.movie)
            if self.movie.isValid(): self.movie.start()
        else:
            # GIF bulunamazsa sabit ikonlara geri dön
            self.set_static_icon()

    def toggle_language(self):
        self.current_language = "en" if self.current_language == "tr" else "tr"
        self.update_ui_language()

    def update_ui_language(self):
        self.disk_label.setText(self.tr("disk"))
        self.format_label.setText(self.tr("format"))
        self.partition_label.setText(self.tr("partition"))
        self.cluster_size_label.setText(self.tr("cluster_size"))
        self.label_label.setText(self.tr("label"))
        self.quick_format_check.setText(self.tr("quick_format"))
        self.format_button.setText(self.tr("format_button"))
        self.about_button.setText(self.tr("about_button"))
        self.label_input.setPlaceholderText(self.tr("label_placeholder"))
        self.update_cluster_size_options()
        

    def show_about_dialog(self):
        # Program içeriği (Dil desteğine göre)
        if self.current_language == "tr":
            description = "Bu program, zengin biçimlendirme seçenekleri ve ayarları ile USB ile bağladığınız flaşbelleklerinize, harddisklerinize ve SSD depolama aygıtlarınıza format atmanızı sağlar."
            warranty = "Bu program hiçbir garanti getirmez."
            version_label = "Sürüm"
        else:
            description = "This program allows you to format your flash drives, hard drives, and SSD storage devices with rich formatting options and settings."
            warranty = "This program comes with absolutely no warranty."
            version_label = "Version"

        html = f"""
        <html><body>
        <h3 style='margin-bottom:0;'>G-USB Formatter</h3>
        <p style='margin-top:5px;'>
        {self.tr('version')}: {APP_VERSION}<br>
        {self.tr('license_label')}: {APP_LICENSE}<br>
        {self.tr('interface')}: Python3 Qt6<br>
        {self.tr('author')}: {AUTHOR_NAME}<br>
        {self.tr('github')}: <a href="https://{GITHUB_URL}" style="text-decoration: none; color: #3498db;">{GITHUB_URL}</a>
        </p>
        <p>{description}</p>
        <p>{warranty}</p>
        <p style='font-size:11px;'>{self.tr('copyright_text')}</p>
        </body></html>
        """
        msg = QMessageBox(self)
        msg.setWindowTitle(self.tr("about_button"))
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(html)
        icon_path = get_resource_path('usb_icon.png')
        if os.path.exists(icon_path):
            msg.setIconPixmap(QPixmap(icon_path).scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        msg.exec()

    def start_format_process(self):
        txt = self.disk_combo.currentText()
        if self.tr("no_usb_found") in txt: return
        path = txt.split()[0]
        fmt = self.format_combo.currentText()
        sch = "msdos" if self.partition_combo.currentText() == "MBR" else "gpt"
        quick = self.quick_format_check.isChecked()
        display_sch = "MBR" if sch == "msdos" else "GPT"
        msg = self.tr("confirm_message").format(path, fmt, display_sch, self.tr("yes") if quick else self.tr("no"))
        reply = QMessageBox.warning(self, self.tr("confirmation"), msg, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.format_button.setEnabled(False)
            self.set_animated_icon()
            self.busy_dialog = BusyDialog(self, self.current_language)
            QTimer.singleShot(300, self.launch_thread)

    def launch_thread(self):
        self.busy_dialog.show()
        path = self.disk_combo.currentText().split()[0]
        self.thread = DiskOperationThread(path, self.format_combo.currentText(), self.cluster_size_combo.currentText(), 
                                          self.label_input.text(), self.quick_format_check.isChecked(), 
                                          self.partition_combo.currentText(), self.current_language)
        self.thread.finished.connect(self.format_finished)
        self.thread.start()

    def format_finished(self, success, message):
        self.format_button.setEnabled(True)
        self.set_static_icon()
        if self.busy_dialog: self.busy_dialog.close()
        if success: QMessageBox.information(self, self.tr("success"), message)
        else: QMessageBox.critical(self, self.tr("error"), message)
        self.load_disks()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = USBFormatterApp()
    ex.show()
    sys.exit(app.exec())