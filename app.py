import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Set page config for a premium wide layout
st.set_page_config(
    page_title="Antenna Gain Calculator | حاسبة كسب الهوائي",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
SPEED_OF_LIGHT = 299792458.0  # m/s

# Custom styling for premium dark theme look, cards, and animations
st.markdown("""
<style>
    /* Premium font loading */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    
    /* Glowing card container */
    .rf-card {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        transition: all 0.3s ease-in-out;
    }
    .rf-card:hover {
        border-color: rgba(139, 92, 246, 0.6);
        box-shadow: 0 8px 32px 0 rgba(139, 92, 246, 0.15);
        transform: translateY(-2px);
    }
    
    /* Neon Text and headings */
    .neon-purple {
        color: #C084FC;
        text-shadow: 0 0 10px rgba(192, 132, 252, 0.3);
    }
    .neon-blue {
        color: #60A5FA;
        text-shadow: 0 0 10px rgba(96, 165, 250, 0.3);
    }
    .neon-green {
        color: #34D399;
        text-shadow: 0 0 10px rgba(52, 211, 153, 0.3);
    }
    
    /* Result styling */
    .result-value {
        font-family: 'Outfit', monospace;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 10px 0;
        background: linear-gradient(135deg, #A78BFA 0%, #60A5FA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Subtitle styling */
    .rf-subtitle {
        color: #94A3B8;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Translation dictionary (Multilingual: Arabic / English / Turkish)
LOCALES = {
    "ar": {
        "title": "📡 حاسبة كسب الهوائيات الذكية",
        "subtitle": "أداة هندسية تفاعلية لحساب كسب الهوائيات باستخدام طرق الانتشار اللاسلكي القياسية.",
        "lang_label": "لغة الواجهة / Language",
        "method_label": "اختر طريقة حساب كسب الهوائي",
        "method_2ant": "طريقة الهوائيين المتطابقين (Two-Antenna Method)",
        "method_3ant": "طريقة الثلاث هوائيات المختلفة (Three-Antenna Method)",
        "method_ref": "طريقة الهوائي المرجعي القياسي (Standard Reference Antenna)",
        "inputs_title": "📥 إدخال البيانات الأساسية",
        "results_title": "📊 النتائج والتحليل الرياضي",
        "freq": "التردد التشغيلي (Frequency)",
        "dist": "المسافة الفاصلة (Distance - d)",
        "pt": "قدرة الإرسال (Transmitted Power - Pt)",
        "pr": "القدرة المستقبلة (Received Power - Pr)",
        "lt": "فقد الكابل المرسل (Tx Cable Loss - Lt)",
        "lr": "فقد الكابل المستقبل (Rx Cable Loss - Lr)",
        "cable_losses": "الخسائر الملحقة (Cable & System Losses)",
        "fspl_calc": "فقد الانتشار في الفضاء الحر (FSPL):",
        "calc_button": "احسب الكسب الآن 🚀",
        "wavelength": "طول الموجة (Wavelength - λ):",
        "gain_result": "كسب الهوائي المحسوب (Gain):",
        "math_steps": "🔍 الخطوات الرياضية بالتفصيل",
        "diagram_title": "⚡ مخطط التوصيل ومسار الإشارة",
        
        # 3-Antenna translations
        "three_ant_desc": "تستخدم هذه الطريقة لحساب كسب 3 هوائيات مختلفة (أ، ب، ج) عن طريق إجراء 3 قياسات ثنائية متعاقبة تحت نفس المسافة والتردد.",
        "pair_ab": "القياس 1: الإرسال بالهوائي (أ) والاستقبال بالهوائي (ب)",
        "pair_bc": "القياس 2: الإرسال بالهوائي (ب) والاستقبال بالهوائي (ج)",
        "pair_ca": "القياس 3: الإرسال بالهوائي (ج) والاستقبال بالهوائي (أ)",
        "gain_a": "كسب الهوائي أ (Gain A)",
        "gain_b": "كسب الهوائي ب (Gain B)",
        "gain_c": "كسب الهوائي ج (Gain C)",
        
        # Reference Antenna translations
        "ref_ant_desc": "تعتمد هذه الطريقة على هوائي معروف الكسب مسبقاً (معياري) لمقارنة الهوائي المجهول به، أو الحساب المباشر بمعرفة كسب أحدهما.",
        "ref_submethod": "نوع الحساب المرجعي",
        "ref_submethod_comp": "طريقة المقارنة والاستبدال (Gain Comparison/Substitution)",
        "ref_submethod_friis": "معادلة فريس المباشرة (معرفة كسب أحد الهوائيين)",
        "g_std_label": "كسب الهوائي القياسي المعروف (Gain of Standard Antenna - Gs)",
        "pr_std_label": "القدرة المستقبلة بالهوائي القياسي (Received Power with Standard - Pr,std)",
        "pr_test_label": "القدرة المستقبلة بالهوائي المجهول (Received Power with Test - Pr,test)",
        "l_std_label": "فقد كابل الهوائي القياسي (Cable Loss - Lstd)",
        "l_test_label": "فقد كابل الهوائي المجهول (Cable Loss - Ltest)",
        "g_known_label": "كسب الهوائي المعروف (Known Antenna Gain)",
        "known_role": "الهوائي المعروف هو:",
        "known_role_tx": "هوائي الإرسال (Tx Antenna)",
        "known_role_rx": "هوائي الاستقبال (Rx Antenna)",
        "unknown_gain_result": "كسب الهوائي المجهول المحسوب:",
        
        # Plot labels
        "plot_title_fspl_freq": "فقد الانتشار في الفضاء الحر vs التردد",
        "plot_title_fspl_dist": "فقد الانتشار في الفضاء الحر vs المسافة",
        "fspl_axis": "فقد الانتشار FSPL (dB)",
        "freq_axis": "التردد",
        "dist_axis": "المسافة",
        
        # Alerts/Errors
        "value_error": "الرجاء التأكد من إدخال قيم موجبة أكبر من الصفر للمسافة والتردد.",
        "power_warning": "القدرة المستقبلة يجب أن تكون منطقياً أقل من القدرة المرسلة في الفضاء الحر.",
        "input_mode_label": "طريقة إدخال الفقد/الإشارة",
        "input_mode_power": "القدرة وخسائر الكابلات (Power & Cable Losses)",
        "input_mode_s": "معامل S21 المباشر من الـ VNA",
        "s21_label": "معامل الانتقال S21 (dB)",
        "mismatch_toggle": "تضمين تصحيح الفقد الناتج عن عدم موائمة المقاومة (S11 / S22)",
        "s11_label": "معامل الانعكاس للمنفذ 1 (S11 بالديسيبل)",
        "s22_label": "معامل الانعكاس للمنفذ 2 (S22 بالديسيبل)",
        "realized_gain_label": "الكسب الفعلي (Realized Gain)",
        "intrinsic_gain_label": "الكسب الصافي (Intrinsic Gain)",
        "mismatch_loss_result": "فقد عدم الموائمة للمنفذ",
        "total_mismatch_loss": "إجمالي فقد عدم الموائمة",
        "s11_error": "معاملات الانعكاس (S11/S22) يجب أن تكون قيمًا سالبة تمامًا (مثال: -10 dB)."
    },
    "en": {
        "title": "📡 Smart Antenna Gain Calculator",
        "subtitle": "Interactive engineering tool for calculating antenna gains using standard RF propagation models.",
        "lang_label": "Interface Language / لغة الواجهة",
        "method_label": "Select Measurement Method",
        "method_2ant": "Identical Two-Antenna Method",
        "method_3ant": "Three-Antenna Method",
        "method_ref": "Standard Reference Antenna Method",
        "inputs_title": "📥 Input Parameters",
        "results_title": "📊 Calculation Results & Analysis",
        "freq": "Operating Frequency",
        "dist": "Antenna Separation Distance (d)",
        "pt": "Transmitted Power (Pt)",
        "pr": "Received Power (Pr)",
        "lt": "Transmitter Cable Loss (Lt)",
        "lr": "Receiver Cable Loss (Lr)",
        "cable_losses": "Cable & System Losses",
        "fspl_calc": "Free Space Path Loss (FSPL):",
        "calc_button": "Calculate Gain 🚀",
        "wavelength": "Wavelength (λ):",
        "gain_result": "Calculated Antenna Gain (Gain):",
        "math_steps": "🔍 Mathematical Step-by-Step Breakdown",
        "diagram_title": "⚡ System Connection & Propagation Diagram",
        
        # 3-Antenna translations
        "three_ant_desc": "Used to find individual gains of 3 different antennas (A, B, C) by conducting 3 pairwise transmission measurements at the same distance & frequency.",
        "pair_ab": "Measurement 1: Tx by Antenna A, Rx by Antenna B",
        "pair_bc": "Measurement 2: Tx by Antenna B, Rx by Antenna C",
        "pair_ca": "Measurement 3: Tx by Antenna C, Rx by Antenna A",
        "gain_a": "Gain of Antenna A",
        "gain_b": "Gain of Antenna B",
        "gain_c": "Gain of Antenna C",
        
        # Reference Antenna translations
        "ref_ant_desc": "Determines the gain of an unknown antenna by comparing it to a known reference standard antenna, or by direct Friis equation if one gain is known.",
        "ref_submethod": "Reference Calculation Type",
        "ref_submethod_comp": "Gain Comparison/Substitution Method",
        "ref_submethod_friis": "Direct Friis Equation (One known antenna)",
        "g_std_label": "Gain of Standard Antenna (Gs)",
        "pr_std_label": "Received Power with Standard Antenna (Pr,std)",
        "pr_test_label": "Received Power with Test Antenna (Pr,test)",
        "l_std_label": "Standard Antenna Cable Loss (Lstd)",
        "l_test_label": "Test Antenna Cable Loss (Ltest)",
        "g_known_label": "Known Antenna Gain",
        "known_role": "The known antenna is:",
        "known_role_tx": "Transmitter Antenna (Tx)",
        "known_role_rx": "Receiver Antenna (Rx)",
        "unknown_gain_result": "Calculated Unknown Antenna Gain:",
        
        # Plot labels
        "plot_title_fspl_freq": "FSPL vs Frequency",
        "plot_title_fspl_dist": "FSPL vs Distance",
        "fspl_axis": "Path Loss FSPL (dB)",
        "freq_axis": "Frequency",
        "dist_axis": "Distance",
        
        # Alerts/Errors
        "value_error": "Please ensure distance and frequency are positive values greater than zero.",
        "power_warning": "Received power should theoretically be lower than transmitted power in passive free space.",
        "input_mode_label": "Transmission Input Mode",
        "input_mode_power": "Power & Cable Losses",
        "input_mode_s": "Direct S21 Parameter from VNA",
        "s21_label": "Transmission Coefficient S21 (dB)",
        "mismatch_toggle": "Include Mismatch Loss Correction (S11 / S22)",
        "s11_label": "Port 1 Reflection Coefficient (S11 in dB)",
        "s22_label": "Port 2 Reflection Coefficient (S22 in dB)",
        "realized_gain_label": "Realized Gain",
        "intrinsic_gain_label": "Intrinsic Gain (Saf Gain)",
        "mismatch_loss_result": "Mismatch Loss for Port",
        "total_mismatch_loss": "Total Mismatch Loss",
        "s11_error": "Reflection coefficients (S11/S22) must be strictly negative values (e.g. -10 dB)."
    },
    "tr": {
        "title": "📡 Akıllı Anten Kazancı Hesaplayıcı",
        "subtitle": "Standart RF yayılım modellerini kullanarak anten kazançlarını hesaplayan etkileşimli mühendislik aracı.",
        "lang_label": "Arayüz Dili / Language / Dil",
        "method_label": "Ölçüm Yöntemini Seçin",
        "method_2ant": "Özdeş İki Anten Yöntemi (Two-Antenna)",
        "method_3ant": "Üç Farklı Anten Yöntemi (Three-Antenna)",
        "method_ref": "Standart Referans Anten Yöntemi (Reference Antenna)",
        "inputs_title": "📥 Giriş Parametreleri",
        "results_title": "📊 Hesaplama Sonuçları ve Analiz",
        "freq": "Çalışma Frekansı (Frequency)",
        "dist": "Antenler Arası Mesafe (Distance - d)",
        "pt": "İletilen Güç (Transmitted Power - Pt)",
        "pr": "Alınan Güç (Received Power - Pr)",
        "lt": "Verici Kablo Kaybı (Tx Cable Loss - Lt)",
        "lr": "Alıcı Kablo Kaybı (Rx Cable Loss - Lr)",
        "cable_losses": "Kablo ve Sistem Kayıpları (System Losses)",
        "fspl_calc": "Serbest Uzay Yol Kaybı (FSPL):",
        "calc_button": "Kazancı Hesapla 🚀",
        "wavelength": "Dalga Boyu (Wavelength - λ):",
        "gain_result": "Hesaplanan Anten Kazancı (Gain):",
        "math_steps": "🔍 Adım Adım Matematiksel Çözüm",
        "diagram_title": "⚡ Sistem Bağlantı ve Yayılım Şeması",
        
        # 3-Antenna translations
        "three_ant_desc": "Bu yöntem, aynı mesafe ve frekansta üç çift ölçüm gerçekleştirerek üç farklı antenin (A, B, C) bireysel kazançlarını bulmak için kullanılır.",
        "pair_ab": "Ölçüm 1: Anten A ile iletim, Anten B ile alım",
        "pair_bc": "Ölçüm 2: Anten B ile iletim, Anten C ile alım",
        "pair_ca": "Ölçüm 3: Anten C ile iletim, Anten A ile alım",
        "gain_a": "Anten A Kazancı (Gain A)",
        "gain_b": "Anten B Kazancı (Gain B)",
        "gain_c": "Anten C Kazancı (Gain C)",
        
        # Reference Antenna translations
        "ref_ant_desc": "Bilinmeyen bir antenin kazancını, kazancı bilinen standart bir referans antenle karşılaştırarak veya bir kazanç biliniyorsa doğrudan Friis formülüyle belirler.",
        "ref_submethod": "Referans Hesaplama Türü",
        "ref_submethod_comp": "Kazanç Karşılaştırma/İkame Yöntemi",
        "ref_submethod_friis": "Doğrudan Friis Denklemi (Bir anteni bilinen)",
        "g_std_label": "Standart Anten Kazancı (Gs)",
        "pr_std_label": "Standart Antenle Alınan Güç (Pr,std)",
        "pr_test_label": "Test Anteniyle Alınan Güç (Pr,test)",
        "l_std_label": "Standart Anten Kablo Kaybı (Lstd)",
        "l_test_label": "Test Anteni Kablo Kaybı (Ltest)",
        "g_known_label": "Bilinen Anten Kazancı",
        "known_role": "Bilinen anten hangisi:",
        "known_role_tx": "Verici Anten (Tx)",
        "known_role_rx": "Alıcı Anten (Rx)",
        "unknown_gain_result": "Hesaplanan Bilinmeyen Anten Kazancı:",
        
        # Plot labels
        "plot_title_fspl_freq": "FSPL vs Frekans",
        "plot_title_fspl_dist": "FSPL vs Mesafe",
        "fspl_axis": "Yol Kaybı FSPL (dB)",
        "freq_axis": "Frekans",
        "dist_axis": "Mesafe",
        
        # Alerts/Errors
        "value_error": "Lütfen mesafe ve frekans için sıfırdan büyük pozitif değerler girdiğinizden emin olun.",
        "power_warning": "Alınan güç, pasif serbest uzayda teorik olarak iletilen güçten daha düşük olmalıdır.",
        "input_mode_label": "İletim Giriş Yöntemi",
        "input_mode_power": "Güç ve Kablo Kayıpları (Power & Cable Losses)",
        "input_mode_s": "VNA'dan Doğrudan S21 Parametresi",
        "s21_label": "İletim Katsayısı S21 (dB)",
        "mismatch_toggle": "Empedans Uyumsuzluk Kaybı Düzeltmesini Ekle (S11 / S22)",
        "s11_label": "Port 1 Yansıma Katsayısı (S11 in dB)",
        "s22_label": "Port 2 Yansıma Katsayısı (S22 in dB)",
        "realized_gain_label": "Gerçekleşen Kazanç (Realized Gain)",
        "intrinsic_gain_label": "Saf Kazanç (Intrinsic Gain)",
        "mismatch_loss_result": "Port için Uyumsuzluk Kaybı",
        "total_mismatch_loss": "Toplam Uyumsuzluk Kaybı",
        "s11_error": "Yansıma katsayıları (S11/S22) sıfırdan küçük negatif değerler olmalıdır (Örn: -10 dB)."
    }
}

# Language selection in Sidebar
st.sidebar.markdown("### 🌐 Settings / الإعدادات / Ayarlar")
lang = st.sidebar.selectbox("Language / اللغة / Dil", ["ar", "en", "tr"], format_func=lambda x: "العربية" if x == "ar" else ("English" if x == "en" else "Türkçe"))
T = LOCALES[lang]

st.title(T["title"])
st.markdown(f"<p class='rf-subtitle'>{T['subtitle']}</p>", unsafe_allow_html=True)

# Select Antenna Gain Measurement Method
method = st.sidebar.radio(
    T["method_label"],
    ["2ant", "3ant", "ref"],
    format_func=lambda x: T["method_2ant"] if x == "2ant" else (T["method_3ant"] if x == "3ant" else T["method_ref"])
)

# Helper unit converters
def convert_power_to_dbm(val, unit):
    if unit == "dBm":
        return val
    elif unit == "dBW":
        return val + 30.0
    elif unit == "W":
        return 10.0 * np.log10(val * 1000.0) if val > 0 else -100.0
    elif unit == "mW":
        return 10.0 * np.log10(val) if val > 0 else -100.0
    return val

def convert_dbm_to_unit(val_dbm, unit):
    if unit == "dBm":
        return val_dbm
    elif unit == "dBW":
        return val_dbm - 30.0
    elif unit == "W":
        return 10.0 ** ((val_dbm - 30.0) / 10.0)
    elif unit == "mW":
        return 10.0 ** (val_dbm / 10.0)
    return val_dbm

def convert_freq_to_hz(val, unit):
    if unit == "Hz":
        return val
    elif unit == "kHz":
        return val * 1e3
    elif unit == "MHz":
        return val * 1e6
    elif unit == "GHz":
        return val * 1e9
    return val

def convert_dist_to_meters(val, unit):
    if unit == "Meters (m)":
        return val
    elif unit == "Feet (ft)":
        return val * 0.3048
    elif unit == "Kilometers (km)":
        return val * 1000.0
    elif unit == "Miles (mi)":
        return val * 1609.344
    return val

def calculate_fspl(freq_hz, dist_m):
    wavelength = SPEED_OF_LIGHT / freq_hz
    return 20 * np.log10(4 * np.pi * dist_m / wavelength)

# SVG Builder for Setup diagram (High Aesthetics, Glowing elements)
def draw_svg_setup(freq_str, dist_str, fspl_val, g_tx, g_rx, loss_t, loss_r):
    svg = f"""
    <svg width="100%" height="180" viewBox="0 0 800 180" xmlns="http://www.w3.org/2000/svg" style="background:#0F172A; border-radius:12px; border: 1px solid rgba(139, 92, 246, 0.25);">
        <!-- Definition of gradients & filters for glow effect -->
        <defs>
            <linearGradient id="waveGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#8B5CF6" stop-opacity="0.8"/>
                <stop offset="50%" stop-color="#3B82F6" stop-opacity="0.8"/>
                <stop offset="100%" stop-color="#34D399" stop-opacity="0.8"/>
            </linearGradient>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="4" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over"/>
            </filter>
        </defs>

        <!-- Tx System Box -->
        <rect x="30" y="50" width="130" height="80" rx="10" fill="#1E293B" stroke="#8B5CF6" stroke-width="2" />
        <text x="95" y="85" fill="#F1F5F9" font-size="13" font-weight="bold" text-anchor="middle">Transmitter (Tx)</text>
        <text x="95" y="105" fill="#A78BFA" font-size="11" text-anchor="middle">Loss: {loss_t} dB</text>

        <!-- Cable Tx -->
        <line x1="160" y1="90" x2="210" y2="90" stroke="#8B5CF6" stroke-dasharray="4" stroke-width="3"/>

        <!-- Tx Antenna -->
        <polygon points="210,90 240,60 240,120" fill="#3B82F6" opacity="0.8"/>
        <line x1="210" y1="90" x2="240" y2="90" stroke="#FFF" stroke-width="2"/>
        <text x="235" y="50" fill="#60A5FA" font-size="11" font-weight="bold" text-anchor="end">Gt: {g_tx}</text>

        <!-- EM Waves Propagation (Glow Effect) -->
        <path d="M 260 70 A 50 50 0 0 1 260 110" fill="none" stroke="url(#waveGrad)" stroke-width="3" filter="url(#glow)"/>
        <path d="M 280 60 A 70 70 0 0 1 280 120" fill="none" stroke="url(#waveGrad)" stroke-width="3" filter="url(#glow)" stroke-dasharray="8 4"/>
        <path d="M 300 50 A 90 90 0 0 1 300 130" fill="none" stroke="url(#waveGrad)" stroke-width="3" filter="url(#glow)"/>
        
        <path d="M 540 70 A 50 50 0 0 0 540 110" fill="none" stroke="url(#waveGrad)" stroke-width="3" filter="url(#glow)"/>
        <path d="M 520 60 A 70 70 0 0 0 520 120" fill="none" stroke="url(#waveGrad)" stroke-width="3" filter="url(#glow)" stroke-dasharray="8 4"/>
        <path d="M 500 50 A 90 90 0 0 0 500 130" fill="none" stroke="url(#waveGrad)" stroke-width="3" filter="url(#glow)"/>

        <!-- Distance Line -->
        <line x1="240" y1="150" x2="560" y2="150" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5 5"/>
        <polygon points="240,150 250,145 250,155" fill="#94A3B8"/>
        <polygon points="560,150 550,145 550,155" fill="#94A3B8"/>
        <text x="400" y="145" fill="#94A3B8" font-size="12" font-weight="bold" text-anchor="middle">Distance (d) = {dist_str}</text>
        
        <!-- Signal / Info in the middle -->
        <rect x="330" y="70" width="140" height="40" rx="8" fill="#0F172A" stroke="#34D399" stroke-width="1.5" />
        <text x="400" y="88" fill="#34D399" font-size="11" font-weight="bold" text-anchor="middle">FSPL = {fspl_val:.2f} dB</text>
        <text x="400" y="103" fill="#94A3B8" font-size="9" text-anchor="middle">Freq: {freq_str}</text>

        <!-- Rx Antenna -->
        <polygon points="590,90 560,60 560,120" fill="#34D399" opacity="0.8"/>
        <line x1="590" y1="90" x2="560" y2="90" stroke="#FFF" stroke-width="2"/>
        <text x="565" y="50" fill="#34D399" font-size="11" font-weight="bold" text-anchor="start">Gr: {g_rx}</text>

        <!-- Cable Rx -->
        <line x1="590" y1="90" x2="640" y2="90" stroke="#34D399" stroke-dasharray="4" stroke-width="3"/>

        <!-- Rx System Box -->
        <rect x="640" y="50" width="130" height="80" rx="10" fill="#1E293B" stroke="#34D399" stroke-width="2" />
        <text x="705" y="85" fill="#F1F5F9" font-size="13" font-weight="bold" text-anchor="middle">Receiver (Rx)</text>
        <text x="705" y="105" fill="#A7F3D0" font-size="11" text-anchor="middle">Loss: {loss_r} dB</text>
    </svg>
    """
    return svg


# -------------------------------------------------------------
# METHOD 1: TWO IDENTICAL ANTENNAS METHOD
# -------------------------------------------------------------
if method == "2ant":
    st.markdown(f"### 📡 {T['method_2ant']}")
    
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        st.markdown(f"<div class='rf-card'><h4>{T['inputs_title']}</h4>", unsafe_allow_html=True)
        
        # Frequency
        f_val = st.number_input(f"{T['freq']}", min_value=0.001, value=2.4, step=0.1, format="%.4f", key="2ant_f")
        f_unit = st.selectbox("Frequency Unit", ["GHz", "MHz", "kHz", "Hz"], key="2ant_f_unit")
        
        # Distance
        d_val = st.number_input(f"{T['dist']}", min_value=0.001, value=5.0, step=0.5, format="%.3f", key="2ant_d")
        d_unit = st.selectbox("Distance Unit", ["Meters (m)", "Feet (ft)", "Kilometers (km)", "Miles (mi)"], key="2ant_d_unit")
        
        # Input mode select (Power & Cable Losses vs Direct S21)
        input_mode = st.radio(
            T["input_mode_label"],
            ["power", "s21"],
            format_func=lambda x: T["input_mode_power"] if x == "power" else T["input_mode_s"],
            key="2ant_input_mode"
        )
        
        pt_val, pt_unit, pr_val, pr_unit = 1.0, "W", -45.0, "dBm"
        lt_val, lr_val = 0.0, 0.0
        s21_val = -26.08
        
        if input_mode == "power":
            # Transmitted Power
            pt_val = st.number_input(f"{T['pt']}", value=1.0, step=0.1, key="2ant_pt")
            pt_unit = st.selectbox("Pt Unit", ["W", "mW", "dBm", "dBW"], key="2ant_pt_unit")
            
            # Received Power
            pr_val = st.number_input(f"{T['pr']}", value=-45.0, step=1.0, key="2ant_pr")
            pr_unit = st.selectbox("Pr Unit", ["dBm", "dBW", "mW", "W"], key="2ant_pr_unit")
            
            # Cable Losses
            with st.expander(T["cable_losses"]):
                lt_val = st.number_input(f"{T['lt']}", min_value=0.0, value=0.0, step=0.1, key="2ant_lt")
                lr_val = st.number_input(f"{T['lr']}", min_value=0.0, value=0.0, step=0.1, key="2ant_lr")
        else:
            s21_val = st.number_input(f"{T['s21_label']}", value=-26.08, step=1.0, format="%.2f", key="2ant_s21")
            
        st.markdown("<hr style='border: 0.5px solid rgba(139,92,246,0.2)'/>", unsafe_allow_html=True)
        include_mismatch = st.checkbox(T["mismatch_toggle"], value=False, key="2ant_mismatch_toggle")
        
        s11_val = -10.0
        s22_val = -10.0
        if include_mismatch:
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                s11_val = st.number_input(T["s11_label"], min_value=-100.0, max_value=-0.01, value=-10.0, step=0.5, format="%.2f", key="2ant_s11")
            with col_m2:
                s22_val = st.number_input(T["s22_label"], min_value=-100.0, max_value=-0.01, value=-10.0, step=0.5, format="%.2f", key="2ant_s22")
                
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"<div class='rf-card'><h4>{T['results_title']}</h4>", unsafe_allow_html=True)
        
        # Convert Units
        f_hz = convert_freq_to_hz(f_val, f_unit)
        d_m = convert_dist_to_meters(d_val, d_unit)
        
        wavelength = SPEED_OF_LIGHT / f_hz
        
        if f_hz <= 0 or d_m <= 0:
            st.error(T["value_error"])
        else:
            # Determine S21 based on input mode
            if input_mode == "power":
                pt_dbm = convert_power_to_dbm(pt_val, pt_unit)
                pr_dbm = convert_power_to_dbm(pr_val, pr_unit)
                if pr_dbm >= pt_dbm:
                    st.warning(T["power_warning"])
                s21_calc = pr_dbm - pt_dbm + lt_val + lr_val
            else:
                s21_calc = s21_val
                pt_dbm = 0.0
                pr_dbm = 0.0
                
            fspl = calculate_fspl(f_hz, d_m)
            
            # Mismatch Loss calculation
            if include_mismatch:
                m1 = 10.0 * np.log10(1.0 - 10.0**(s11_val / 10.0))
                m2 = 10.0 * np.log10(1.0 - 10.0**(s22_val / 10.0))
                m_total = m1 + m2
            else:
                m1 = 0.0
                m2 = 0.0
                m_total = 0.0
                
            # Gain calculation
            g_realized = (s21_calc + fspl) / 2.0
            g_intrinsic = (s21_calc + fspl - m1 - m2) / 2.0
            
            # Visual result cards
            if include_mismatch:
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 10px; background: rgba(96,165,250,0.1); border-radius: 12px; margin-bottom: 20px; border: 1px dashed rgba(96,165,250,0.4)">
                        <span style="font-size: 1.0rem; color: #60A5FA;">{T['realized_gain_label']}</span>
                        <div class="result-value" style="font-size: 2.2rem; background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{g_realized:.3f} dBi</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_g2:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 10px; background: rgba(52,211,153,0.1); border-radius: 12px; margin-bottom: 20px; border: 1px dashed rgba(52,211,153,0.4)">
                        <span style="font-size: 1.0rem; color: #34D399;">{T['intrinsic_gain_label']}</span>
                        <div class="result-value" style="font-size: 2.2rem; background: linear-gradient(135deg, #34D399 0%, #10B981 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{g_intrinsic:.3f} dBi</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="text-align: center; padding: 10px; background: rgba(139,92,246,0.1); border-radius: 12px; margin-bottom: 20px; border: 1px dashed rgba(139,92,246,0.4)">
                    <span style="font-size: 1.1rem; color: #A78BFA;">{T['gain_result']}</span>
                    <div class="result-value">{g_realized:.3f} dBi</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Wavelength and Path loss info
            col_res1, col_res2 = st.columns(2)
            col_res1.metric(T["wavelength"], f"{wavelength:.5f} m")
            col_res2.metric(T["fspl_calc"], f"{fspl:.2f} dB")
            
            if include_mismatch:
                col_m_res1, col_m_res2, col_m_res3 = st.columns(3)
                col_m_res1.metric(f"M1 ({T['mismatch_loss_result']} 1)", f"{m1:.3f} dB")
                col_m_res2.metric(f"M2 ({T['mismatch_loss_result']} 2)", f"{m2:.3f} dB")
                col_m_res3.metric(T["total_mismatch_loss"], f"{m_total:.3f} dB")
            
            # Connections diagram
            st.markdown(f"<h5>{T['diagram_title']}</h5>", unsafe_allow_html=True)
            if include_mismatch:
                g_tx_str = f"R:{g_realized:.2f} / I:{g_intrinsic:.2f}"
                g_rx_str = f"R:{g_realized:.2f} / I:{g_intrinsic:.2f}"
                if input_mode == "power":
                    loss_t_str = f"{lt_val:.1f} (S11:{s11_val:.1f})"
                    loss_r_str = f"{lr_val:.1f} (S22:{s22_val:.1f})"
                else:
                    loss_t_str = f"0.0 (S11:{s11_val:.1f})"
                    loss_r_str = f"0.0 (S22:{s22_val:.1f})"
            else:
                g_tx_str = f"{g_realized:.2f} dBi"
                g_rx_str = f"{g_realized:.2f} dBi"
                if input_mode == "power":
                    loss_t_str = f"{lt_val:.1f}"
                    loss_r_str = f"{lr_val:.1f}"
                else:
                    loss_t_str = "0.0"
                    loss_r_str = "0.0"
                    
            svg_html = draw_svg_setup(f"{f_val} {f_unit}", f"{d_val} {d_unit.split()[0]}", fspl, g_tx_str, g_rx_str, loss_t_str, loss_r_str)
            st.components.v1.html(svg_html, height=190)
            
            # Mathematical Breakdown
            with st.expander(T["math_steps"]):
                mismatch_math_str = ""
                if include_mismatch:
                    mismatch_math_str = f"""
                **4. Calculate Mismatch Loss (ML) from S11 and S22:**
                - Port 1 Mismatch Loss ($M_1$):
                  $$M_1 = 10 \\log_{{10}}\\left(1 - 10^{{\\frac{{S_{{11}}}}{{10}}}}\\right) = 10 \\log_{{10}}\\left(1 - 10^{{\\frac{{{s11_val:.3f}}}{{10}}}}\\right) = {m1:.3f}\\text{{ dB}}$$
                - Port 2 Mismatch Loss ($M_2$):
                  $$M_2 = 10 \\log_{{10}}\\left(1 - 10^{{\\frac{{S_{{22}}}}{{10}}}}\\right) = 10 \\log_{{10}}\\left(1 - 10^{{\\frac{{{s22_val:.3f}}}{{10}}}}\\right) = {m2:.3f}\\text{{ dB}}$$
                - Total Mismatch Loss:
                  $$M_{{total}} = M_1 + M_2 = {m1:.3f} + ({m2:.3f}) = {m_total:.3f}\\text{{ dB}}$$
                
                **5. Calculate Intrinsic Gain (Corrected for Mismatch Losses):**
                $$S_{{21}} = G_{{tx(int)}} + G_{{rx(int)}} + M_1 + M_2 - FSPL$$
                Assuming identical antennas ($G_{{tx(int)}} = G_{{rx(int)}} = G_{{intrinsic}}$):
                $$2G_{{intrinsic}} = S_{{21}} + FSPL - M_1 - M_2$$
                $$G_{{intrinsic}} = \\frac{{{s21_calc:.3f} + {fspl:.3f} - ({m1:.3f}) - ({m2:.3f})}}{{2}} = {g_intrinsic:.3f}\\text{{ dBi}}$$
                    """
                
                s21_formula_str = ""
                if input_mode == "power":
                    s21_formula_str = f"""
                - Transmitted Power ($P_t$): {pt_val} {pt_unit} $\\rightarrow$ {pt_dbm:.2f} dBm
                - Received Power ($P_r$): {pr_val} {pr_unit} $\\rightarrow$ {pr_dbm:.2f} dBm
                - Tx Cable Loss ($L_t$): {lt_val:.2f} dB, Rx Cable Loss ($L_r$): {lr_val:.2f} dB
                - Transmission Coefficient ($S_{{21}}$):
                  $$S_{{21}} = P_r - P_t + L_t + L_r = {pr_dbm:.2f} - ({pt_dbm:.2f}) + {lt_val:.2f} + {lr_val:.2f} = {s21_calc:.3f}\\text{{ dB}}$$
                    """
                else:
                    s21_formula_str = f"""
                - Transmission Coefficient ($S_{{21}}$): {s21_calc:.2f} dB (Direct Input)
                    """
                    
                st.markdown(f"""
                **1. Convert all units to standard values:**
                - Frequency ($f$): {f_val} {f_unit} $\\rightarrow$ {f_hz:,.1f} Hz
                - Wavelength ($\\lambda = c/f$): ${SPEED_OF_LIGHT} / {f_hz:,.1f} = {wavelength:.6f}$ m
                - Distance ($R$): {d_val} {d_unit} $\\rightarrow$ {d_m:.3f} m
                {s21_formula_str}
                
                **2. Calculate Free Space Path Loss (FSPL):**
                $$FSPL = 20 \\log_{{10}}\\left(\\frac{{4 \\pi R}}{{\\lambda}}\\right) = 20 \\log_{{10}}\\left(\\frac{{4 \\pi \\times {d_m:.3f}}}{{{wavelength:.6f}}}\\right) = {fspl:.3f}\\text{{ dB}}$$
                
                **3. Calculate Realized Gain (Including Mismatch Losses):**
                $$S_{{21}} = G_{{tx(real)}} + G_{{rx(real)}} - FSPL$$
                Assuming identical antennas ($G_{{tx(real)}} = G_{{rx(real)}} = G_{{realized}}$):
                $$2G_{{realized}} = S_{{21}} + FSPL$$
                $$G_{{realized}} = \\frac{{{s21_calc:.3f} + {fspl:.3f}}}{{2}} = {g_realized:.3f}\\text{{ dBi}}$$
                {mismatch_math_str}
                """)
                
        st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------------------
# METHOD 2: THREE DIFFERENT ANTENNAS METHOD
# -------------------------------------------------------------
elif method == "3ant":
    st.markdown(f"### 📡 {T['method_3ant']}")
    st.info(T["three_ant_desc"])
    
    col1, col2 = st.columns([1.1, 1], gap="large")
    
    with col1:
        st.markdown(f"<div class='rf-card'><h4>{T['inputs_title']}</h4>", unsafe_allow_html=True)
        
        # Environmental settings
        row_e1, row_e2 = st.columns(2)
        with row_e1:
            f_val = st.number_input(f"{T['freq']}", min_value=0.001, value=5.8, step=0.1, format="%.4f", key="3ant_f")
            f_unit = st.selectbox("Frequency Unit", ["GHz", "MHz", "kHz", "Hz"], key="3ant_f_unit")
        with row_e2:
            d_val = st.number_input(f"{T['dist']}", min_value=0.001, value=10.0, step=0.5, format="%.3f", key="3ant_d")
            d_unit = st.selectbox("Distance Unit", ["Meters (m)", "Feet (ft)", "Kilometers (km)", "Miles (mi)"], key="3ant_d_unit")
            
        st.markdown("<hr style='border: 0.5px solid rgba(139,92,246,0.2)'/>", unsafe_allow_html=True)
        
        # Common TX power & cable losses
        row_c1, row_c2, row_c3 = st.columns(3)
        with row_c1:
            pt_val = st.number_input(f"{T['pt']}", value=15.0, step=1.0, key="3ant_pt")
            pt_unit = st.selectbox("Pt Unit", ["dBm", "dBW", "W", "mW"], key="3ant_pt_unit")
        with row_c2:
            lt_val = st.number_input(f"{T['lt']}", min_value=0.0, value=0.5, step=0.1, key="3ant_lt")
        with row_c3:
            lr_val = st.number_input(f"{T['lr']}", min_value=0.0, value=0.5, step=0.1, key="3ant_lr")
            
        st.markdown("<hr style='border: 0.5px solid rgba(139,92,246,0.2)'/>", unsafe_allow_html=True)
        
        # 3 Pair measurements
        st.markdown(f"##### {T['pair_ab']}")
        pr_ab = st.number_input(f"{T['pr']} (A-B)", value=-30.0, step=1.0, key="3ant_pr_ab")
        
        st.markdown(f"##### {T['pair_bc']}")
        pr_bc = st.number_input(f"{T['pr']} (B-C)", value=-32.0, step=1.0, key="3ant_pr_bc")
        
        st.markdown(f"##### {T['pair_ca']}")
        pr_ca = st.number_input(f"{T['pr']} (C-A)", value=-28.0, step=1.0, key="3ant_pr_ca")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"<div class='rf-card'><h4>{T['results_title']}</h4>", unsafe_allow_html=True)
        
        f_hz = convert_freq_to_hz(f_val, f_unit)
        d_m = convert_dist_to_meters(d_val, d_unit)
        pt_dbm = convert_power_to_dbm(pt_val, pt_unit)
        
        # Received powers conversions
        pr_ab_dbm = convert_power_to_dbm(pr_ab, "dBm")
        pr_bc_dbm = convert_power_to_dbm(pr_bc, "dBm")
        pr_ca_dbm = convert_power_to_dbm(pr_ca, "dBm")
        
        if f_hz <= 0 or d_m <= 0:
            st.error(T["value_error"])
        else:
            fspl = calculate_fspl(f_hz, d_m)
            
            # Net gains (W_ij)
            w_ab = pr_ab_dbm - pt_dbm + fspl + lt_val + lr_val
            w_bc = pr_bc_dbm - pt_dbm + fspl + lt_val + lr_val
            w_ca = pr_ca_dbm - pt_dbm + fspl + lt_val + lr_val
            
            # Solve system
            g_A = (w_ab - w_bc + w_ca) / 2.0
            g_B = (w_ab + w_bc - w_ca) / 2.0
            g_C = (-w_ab + w_bc + w_ca) / 2.0
            
            # Display gains
            st.markdown(f"""
            <div style="display: flex; flex-direction: column; gap: 15px; margin-bottom: 20px;">
                <div style="padding: 12px; background: rgba(96,165,250,0.1); border-radius: 10px; border-left: 5px solid #60A5FA;">
                    <span style="font-size: 1rem; color: #93C5FD;">{T['gain_a']}</span>
                    <div style="font-size: 1.8rem; font-weight:bold; color: #F1F5F9;">{g_A:.3f} dBi</div>
                </div>
                <div style="padding: 12px; background: rgba(167,139,250,0.1); border-radius: 10px; border-left: 5px solid #A78BFA;">
                    <span style="font-size: 1rem; color: #C084FC;">{T['gain_b']}</span>
                    <div style="font-size: 1.8rem; font-weight:bold; color: #F1F5F9;">{g_B:.3f} dBi</div>
                </div>
                <div style="padding: 12px; background: rgba(52,211,153,0.1); border-radius: 10px; border-left: 5px solid #34D399;">
                    <span style="font-size: 1rem; color: #A7F3D0;">{T['gain_c']}</span>
                    <div style="font-size: 1.8rem; font-weight:bold; color: #F1F5F9;">{g_C:.3f} dBi</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.metric(T["fspl_calc"], f"{fspl:.2f} dB")
            
            # Mathematical Breakdown
            with st.expander(T["math_steps"]):
                st.markdown(f"""
                **1. System Constants & Path Loss:**
                - Frequency: {f_val} {f_unit} $\\rightarrow$ {f_hz:,.1f} Hz
                - Distance: {d_val} {d_unit} $\\rightarrow$ {d_m:.3f} m
                - FSPL: $20 \\log_{{10}}\\left(\\frac{{4 \\pi \\times {d_m:.3f}}}{{\\lambda}}\\right) = {fspl:.3f}$ dB
                - Common $P_t$: {pt_val} {pt_unit} $\\rightarrow$ {pt_dbm:.2f} dBm
                
                **2. Formulating Equations:**
                - $W_{{AB}} = P_{{r,AB}} - P_t + FSPL + L_t + L_r$
                  $W_{{AB}} = {pr_ab_dbm:.2f} - ({pt_dbm:.2f}) + {fspl:.2f} + {lt_val:.2f} + {lr_val:.2f} = {w_ab:.3f}$ dB
                - $W_{{BC}} = P_{{r,BC}} - P_t + FSPL + L_t + L_r$
                  $W_{{BC}} = {pr_bc_dbm:.2f} - ({pt_dbm:.2f}) + {fspl:.2f} + {lt_val:.2f} + {lr_val:.2f} = {w_bc:.3f}$ dB
                - $W_{{CA}} = P_{{r,CA}} - P_t + FSPL + L_t + L_r$
                  $W_{{CA}} = {pr_ca_dbm:.2f} - ({pt_dbm:.2f}) + {fspl:.2f} + {lt_val:.2f} + {lr_val:.2f} = {w_ca:.3f}$ dB
                
                **3. Linear Equation Solving:**
                - $G_A + G_B = {w_ab:.3f}$
                - $G_B + G_C = {w_bc:.3f}$
                - $G_C + G_A = {w_ca:.3f}$
                
                **Solutions:**
                - $G_A = \\frac{{W_{{AB}} - W_{{BC}} + W_{{CA}}}}{{2}} = \\frac{{{w_ab:.2f} - ({w_bc:.2f}) + {w_ca:.2f}}}{{2}} = {g_A:.3f}$ dBi
                - $G_B = \\frac{{W_{{AB}} + W_{{BC}} - W_{{CA}}}}{{2}} = \\frac{{{w_ab:.2f} + ({w_bc:.2f}) - {w_ca:.2f}}}{{2}} = {g_B:.3f}$ dBi
                - $G_C = \\frac{{-W_{{AB}} + W_{{BC}} + W_{{CA}}}}{{2}} = \\frac{{-({w_ab:.2f}) + {w_bc:.2f} + {w_ca:.2f}}}{{2}} = {g_C:.3f}$ dBi
                """)
                
        st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------------------
# METHOD 3: STANDARD REFERENCE ANTENNA METHOD
# -------------------------------------------------------------
elif method == "ref":
    st.markdown(f"### 📡 {T['method_ref']}")
    st.info(T["ref_ant_desc"])
    
    # Select submethod
    submethod = st.sidebar.selectbox(
        T["ref_submethod"],
        ["comp", "friis"],
        format_func=lambda x: T["ref_submethod_comp"] if x == "comp" else T["ref_submethod_friis"]
    )
    
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    if submethod == "comp":
        with col1:
            st.markdown(f"<div class='rf-card'><h4>{T['inputs_title']}</h4>", unsafe_allow_html=True)
            
            g_std = st.number_input(T["g_std_label"], value=10.0, step=0.5, format="%.2f")
            pr_std = st.number_input(T["pr_std_label"], value=-40.0, step=1.0)
            pr_test = st.number_input(T["pr_test_label"], value=-35.0, step=1.0)
            
            with st.expander(T["cable_losses"]):
                l_std = st.number_input(T["l_std_label"], min_value=0.0, value=0.0, step=0.1)
                l_test = st.number_input(T["l_test_label"], min_value=0.0, value=0.0, step=0.1)
                
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"<div class='rf-card'><h4>{T['results_title']}</h4>", unsafe_allow_html=True)
            
            # G_test = G_std + (P_r,test - P_r,std) + (L_test - L_std)
            g_test_dBi = g_std + (pr_test - pr_std) + (l_test - l_std)
            
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; background: rgba(52,211,153,0.1); border-radius: 12px; margin-bottom: 20px; border: 1px dashed rgba(52,211,153,0.4)">
                <span style="font-size: 1.1rem; color: #34D399;">{T['unknown_gain_result']}</span>
                <div class="result-value">{g_test_dBi:.3f} dBi</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander(T["math_steps"]):
                st.markdown(f"""
                **Gain Comparison / Substitution formula:**
                $$G_{{test}} = G_{{std}} + (P_{{r,test}} - P_{{r,std}}) + (L_{{test}} - L_{{std}})$$
                
                **Calculation details:**
                - Known Standard Gain ($G_{{std}}$): {g_std:.2f} dBi
                - Received power difference: ${pr_test:.2f} - ({pr_std:.2f}) = {pr_test - pr_std:.2f}$ dB
                - Cable loss difference: ${l_test:.2f} - {l_std:.2f} = {l_test - l_std:.2f}$ dB
                - $G_{{test}} = {g_std:.2f} + ({pr_test - pr_std:.2f}) + ({l_test - l_std:.2f}) = {g_test_dBi:.3f}$ dBi
                """)
            st.markdown("</div>", unsafe_allow_html=True)
            
    elif submethod == "friis":
        with col1:
            st.markdown(f"<div class='rf-card'><h4>{T['inputs_title']}</h4>", unsafe_allow_html=True)
            
            role = st.selectbox(T["known_role"], ["tx", "rx"], format_func=lambda x: T["known_role_tx"] if x == "tx" else T["known_role_rx"])
            g_known = st.number_input(T["g_known_label"], value=12.0, step=0.5)
            
            f_val = st.number_input(f"{T['freq']}", min_value=0.001, value=2.4, step=0.1, format="%.4f", key="ref_f")
            f_unit = st.selectbox("Frequency Unit", ["GHz", "MHz", "kHz", "Hz"], key="ref_f_unit")
            
            d_val = st.number_input(f"{T['dist']}", min_value=0.001, value=5.0, step=0.5, format="%.3f", key="ref_d")
            d_unit = st.selectbox("Distance Unit", ["Meters (m)", "Feet (ft)", "Kilometers (km)", "Miles (mi)"], key="ref_d_unit")
            
            pt_val = st.number_input(f"{T['pt']}", value=0.1, step=0.01, format="%.4f", key="ref_pt")
            pt_unit = st.selectbox("Pt Unit", ["W", "mW", "dBm", "dBW"], key="ref_pt_unit")
            
            pr_val = st.number_input(f"{T['pr']}", value=-50.0, step=1.0, key="ref_pr")
            pr_unit = st.selectbox("Pr Unit", ["dBm", "dBW", "mW", "W"], key="ref_pr_unit")
            
            with st.expander(T["cable_losses"]):
                lt_val = st.number_input(f"{T['lt']}", min_value=0.0, value=0.0, step=0.1, key="ref_lt")
                lr_val = st.number_input(f"{T['lr']}", min_value=0.0, value=0.0, step=0.1, key="ref_lr")
                
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"<div class='rf-card'><h4>{T['results_title']}</h4>", unsafe_allow_html=True)
            
            f_hz = convert_freq_to_hz(f_val, f_unit)
            d_m = convert_dist_to_meters(d_val, d_unit)
            pt_dbm = convert_power_to_dbm(pt_val, pt_unit)
            pr_dbm = convert_power_to_dbm(pr_val, pr_unit)
            
            if f_hz <= 0 or d_m <= 0:
                st.error(T["value_error"])
            else:
                fspl = calculate_fspl(f_hz, d_m)
                
                # G_unknown = Pr - Pt + FSPL + Lt + Lr - G_known
                g_unknown_dBi = pr_dbm - pt_dbm + fspl + lt_val + lr_val - g_known
                
                st.markdown(f"""
                <div style="text-align: center; padding: 10px; background: rgba(96,165,250,0.1); border-radius: 12px; margin-bottom: 20px; border: 1px dashed rgba(96,165,250,0.4)">
                    <span style="font-size: 1.1rem; color: #93C5FD;">{T['unknown_gain_result']}</span>
                    <div class="result-value">{g_unknown_dBi:.3f} dBi</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Setup diagrams
                st.markdown(f"<h5>{T['diagram_title']}</h5>", unsafe_allow_html=True)
                if role == "tx":
                    svg_html = draw_svg_setup(f"{f_val} {f_unit}", f"{d_val} {d_unit.split()[0]}", fspl, f"{g_known:.2f} dBi (Known)", f"{g_unknown_dBi:.2f} dBi (Unknown)", lt_val, lr_val)
                else:
                    svg_html = draw_svg_setup(f"{f_val} {f_unit}", f"{d_val} {d_unit.split()[0]}", fspl, f"{g_unknown_dBi:.2f} dBi (Unknown)", f"{g_known:.2f} dBi (Known)", lt_val, lr_val)
                st.components.v1.html(svg_html, height=190)
                
                with st.expander(T["math_steps"]):
                    st.markdown(f"""
                    **Direct Friis equation formulation:**
                    $$P_r = P_t + G_{{tx}} + G_{{rx}} - FSPL - L_t - L_r$$
                    
                    **Solving for unknown gain:**
                    $$G_{{unknown}} = P_r - P_t + FSPL + L_t + L_r - G_{{known}}$$
                    
                    **Calculation details:**
                    - Frequency ($f$): {f_hz:,.1f} Hz
                    - Distance ($d$): {d_m:.3f} m
                    - FSPL: {fspl:.3f} dB
                    - Transmitted Power ($P_t$): {pt_dbm:.2f} dBm
                    - Received Power ($P_r$): {pr_dbm:.2f} dBm
                    - Known Gain ($G_{{known}}$): {g_known:.2f} dBi
                    - $G_{{unknown}} = {pr_dbm:.2f} - ({pt_dbm:.2f}) + {fspl:.2f} + {lt_val:.2f} + {lr_val:.2f} - {g_known:.2f} = {g_unknown_dBi:.3f}$ dBi
                    """)
                st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# DYNAMIC VISUALIZATIONS SECTION
# -------------------------------------------------------------
st.markdown("---")
st.markdown(f"### 📈 {T['results_title']}")

# We only draw plots if the operating frequency and distance are configured (i.e. method is 2ant, 3ant, or ref-friis)
has_env = True
if method == "ref" and submethod == "comp":
    has_env = False

if has_env:
    # Set frequency range (e.g. from 0.5x to 2x operating frequency)
    # Generate Plotly charts
    freq_center = f_hz
    dist_center = d_m
    
    tab1, tab2 = st.tabs([T["plot_title_fspl_freq"], T["plot_title_fspl_dist"]])
    
    with tab1:
        # FSPL vs Frequency
        freqs_hz = np.linspace(max(1e3, freq_center * 0.1), freq_center * 3, 200)
        fspl_y = 20 * np.log10(4 * np.pi * dist_center / (SPEED_OF_LIGHT / freqs_hz))
        
        # Human readable labels for Plotly x axis
        if f_unit == "GHz":
            freqs_plot = freqs_hz / 1e9
            x_title = f"{T['freq_axis']} (GHz)"
            center_x = freq_center / 1e9
        elif f_unit == "MHz":
            freqs_plot = freqs_hz / 1e6
            x_title = f"{T['freq_axis']} (MHz)"
            center_x = freq_center / 1e6
        elif f_unit == "kHz":
            freqs_plot = freqs_hz / 1e3
            x_title = f"{T['freq_axis']} (kHz)"
            center_x = freq_center / 1e3
        else:
            freqs_plot = freqs_hz
            x_title = f"{T['freq_axis']} (Hz)"
            center_x = freq_center
            
        fig_freq = go.Figure()
        # Path Loss curve
        fig_freq.add_trace(go.Scatter(
            x=freqs_plot, y=fspl_y,
            mode='lines',
            line=dict(color='#8B5CF6', width=3),
            name="FSPL"
        ))
        # Highlight operating point
        fig_freq.add_trace(go.Scatter(
            x=[center_x], y=[calculate_fspl(freq_center, dist_center)],
            mode='markers+text',
            marker=dict(color='#34D399', size=12, line=dict(color='#FFFFFF', width=2)),
            text=[f"Operating Point ({center_x:.2f}, {calculate_fspl(freq_center, dist_center):.1f} dB)"],
            textposition="top center",
            name="Operating Pt"
        ))
        
        fig_freq.update_layout(
            title=T["plot_title_fspl_freq"],
            xaxis_title=x_title,
            yaxis_title=T["fspl_axis"],
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Outfit, sans-serif"),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_freq, use_container_width=True)
        
    with tab2:
        # FSPL vs Distance
        dists_m = np.linspace(max(0.1, dist_center * 0.1), dist_center * 3, 200)
        fspl_dist_y = 20 * np.log10(4 * np.pi * dists_m / (SPEED_OF_LIGHT / freq_center))
        
        if d_unit == "Meters (m)":
            dists_plot = dists_m
            x_title = f"{T['dist_axis']} (m)"
            center_d_x = dist_center
        elif d_unit == "Feet (ft)":
            dists_plot = dists_m / 0.3048
            x_title = f"{T['dist_axis']} (ft)"
            center_d_x = dist_center / 0.3048
        elif d_unit == "Kilometers (km)":
            dists_plot = dists_m / 1000.0
            x_title = f"{T['dist_axis']} (km)"
            center_d_x = dist_center / 1000.0
        else:
            dists_plot = dists_m / 1609.344
            x_title = f"{T['dist_axis']} (mi)"
            center_d_x = dist_center / 1609.344
            
        fig_dist = go.Figure()
        # Path Loss curve
        fig_dist.add_trace(go.Scatter(
            x=dists_plot, y=fspl_dist_y,
            mode='lines',
            line=dict(color='#60A5FA', width=3),
            name="FSPL"
        ))
        # Highlight operating point
        fig_dist.add_trace(go.Scatter(
            x=[center_d_x], y=[calculate_fspl(freq_center, dist_center)],
            mode='markers+text',
            marker=dict(color='#34D399', size=12, line=dict(color='#FFFFFF', width=2)),
            text=[f"Operating Point ({center_d_x:.2f}, {calculate_fspl(freq_center, dist_center):.1f} dB)"],
            textposition="top center",
            name="Operating Pt"
        ))
        
        fig_dist.update_layout(
            title=T["plot_title_fspl_dist"],
            xaxis_title=x_title,
            yaxis_title=T["fspl_axis"],
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Outfit, sans-serif"),
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_dist, use_container_width=True)
else:
    # If comparison method, show simple explanation or generic plots
    st.info("Operating frequency and distance plots are not applicable in standard substitution/comparison mode as they are cancel-out variables.")
