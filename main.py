from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
import random

class DiagnosticApp(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        
        # إنشاء التبويبات
        self.add_widget(self.create_fuel_tab())
        self.add_widget(self.create_diagnostic_tab())
        self.add_widget(self.create_obd_tab())    def create_fuel_tab(self):
        # تبويب حساب الوقود
        fuel_tab = BoxLayout(orientation='vertical', padding=10, spacing=10)
        fuel_tab.add_widget(Label(text='حساب استهلاك الوقود', size_hint_y=0.1, font_size='20sp'))
        
        # حقل إدخال المسافة
        distance_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        distance_layout.add_widget(Label(text='المسافة (كم):', size_hint_x=0.4))
        self.distance_input = TextInput(multiline=False, input_filter='float')
        distance_layout.add_widget(self.distance_input)
        fuel_tab.add_widget(distance_layout)
        
        # حقل إدخال استهلاك الوقود
        consumption_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        consumption_layout.add_widget(Label(text='استهلاك الوقود (لتر/100كم):', size_hint_x=0.4))
        self.consumption_input = TextInput(multiline=False, input_filter='float')
        consumption_layout.add_widget(self.consumption_input)
        fuel_tab.add_widget(consumption_layout)
        
        # حقل إدخال سعر الوقود
        price_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        price_layout.add_widget(Label(text='سعر اللتر (ريال):', size_hint_x=0.4))
        self.price_input = TextInput(multiline=False, input_filter='float')
        price_layout.add_widget(self.price_input)
        fuel_tab.add_widget(price_layout)
        
        # زر الحساب
        calculate_btn = Button(text='احسب التكلفة', size_hint_y=0.1)
        calculate_btn.bind(on_press=self.calculate_fuel)
        fuel_tab.add_widget(calculate_btn)
        
        # منطقة النتائج
        self.result_label = Label(text='النتيجة ستظهر هنا', size_hint_y=0.2, halign='center')
        fuel_tab.add_widget(self.result_label)
        
        return fuel_tab
          def create_diagnostic_tab(self):
        # تبويب الفحص اليدوي
        diagnostic_tab = BoxLayout(orientation='vertical', padding=10, spacing=10)
        diagnostic_tab.add_widget(Label(text='الفحص اليدوي للسيارة', size_hint_y=0.1, font_size='20sp'))
        
        # قائمة الفحص
        scroll = ScrollView()
        self.checklist_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.checklist_layout.bind(minimum_height=self.checklist_layout.setter('height'))
        
        checklist_items = [
            'المحرك: استمع لأي أصوات غير طبيعية',
            'زيت المحرك: تحقق من المستوى واللون',
            'الإطارات: تحقق من الضغط والتآكل',
            'الفرامل: اختبر كفاءة الفرملة',
            'الإضاءة: تحقق من كل المصابيح',
            'المبرد: تحقق من مستوى سائل التبريد',
            'البطارية: تحقق من التوصيلات والنظافة',
            'حزام المحرك: تحقق من الشد والتآكل'
        ]
        
        self.check_buttons = []
        for item in checklist_items:
            btn = Button(text=item, size_hint_y=None, height=60)
            btn.checked = False
            btn.bind(on_press=self.toggle_check)
            self.checklist_layout.add_widget(btn)
            self.check_buttons.append(btn)
        
        scroll.add_widget(self.checklist_layout)
        diagnostic_tab.add_widget(scroll)
        
        # نتيجة الفحص
        self.diagnostic_result = Label(text='اكتمل 0% من الفحص', size_hint_y=0.1)
        diagnostic_tab.add_widget(self.diagnostic_result)
        
        self.progress_bar = ProgressBar(max=100, size_hint_y=0.05)
        diagnostic_tab.add_widget(self.progress_bar)
        
        return diagnostic_tab
          def create_obd_tab(self):
        # تبويب OBD-II
        obd_tab = BoxLayout(orientation='vertical', padding=10, spacing=10)
        obd_tab.add_widget(Label(text='نظام OBD-II', size_hint_y=0.1, font_size='20sp'))
        
        # محاكاة بيانات OBD
        self.obd_data_label = Label(
            text='اضغط "بدء المسح" لجمع بيانات السيارة\n\n'
                 'سرعة المحرك: -- RPM\n'
                 'درجة الحرارة: -- °C\n'
                 'سرعة السيارة: -- km/h\n'
                 'حمل المحرك: -- %\n'
                 'ضغط الوقود: -- kPa',
            size_hint_y=0.4,
            halign='center'
        )
        obd_tab.add_widget(self.obd_data_label)
        
        # أزرار التحكم
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        
        start_scan_btn = Button(text='بدء المسح')
        start_scan_btn.bind(on_press=self.start_obd_scan)
        buttons_layout.add_widget(start_scan_btn)
        
        clear_btn = Button(text='مسح')
        clear_btn.bind(on_press=self.clear_obd_data)
        buttons_layout.add_widget(clear_btn)
        
        obd_tab.add_widget(buttons_layout)
        
        # منطقة رموز الأعطال
        self.error_codes_label = Label(text='لا توجد رموز أعطال', size_hint_y=0.3)
        obd_tab.add_widget(self.error_codes_label)
        
        return obd_tab
          def calculate_fuel(self, instance):
        try:
            distance = float(self.distance_input.text)
            consumption = float(self.consumption_input.text)
            price = float(self.price_input.text)
            
            fuel_used = (consumption / 100) * distance
            total_cost = fuel_used * price
            
            self.result_label.text = f'''
المسافة: {distance} كم
الاستهلاك: {consumption} لتر/100كم
كمية الوقود: {fuel_used:.2f} لتر
التكلفة الإجمالية: {total_cost:.2f} ريال
'''
        except ValueError:
            self.result_label.text = 'يرجى إدخال قيم صحيحة'
    
    def toggle_check(self, instance):
        instance.checked = not instance.checked
        if instance.checked:
            instance.background_color = (0, 1, 0, 1)  # أخضر
        else:
            instance.background_color = (1, 1, 1, 1)  # أبيض
        
        self.update_diagnostic_progress()
    
    def update_diagnostic_progress(self):
        checked_count = sum(1 for btn in self.check_buttons if btn.checked)
        total_count = len(self.check_buttons)
        progress = (checked_count / total_count) * 100
        
        self.progress_bar.value = progress
        self.diagnostic_result.text = f'اكتمل {progress:.1f}% من الفحص'
          def start_obd_scan(self, instance):
        # محاكاة بيانات OBD-II
        engine_rpm = random.randint(800, 3000)
        engine_temp = random.randint(85, 105)
        vehicle_speed = random.randint(0, 120)
        engine_load = random.randint(20, 80)
        fuel_pressure = random.randint(300, 800)
        
        self.obd_data_label.text = f'''
بيانات OBD-II المحدثة:\n
سرعة المحرك: {engine_rpm} RPM
درجة الحرارة: {engine_temp} °C
سرعة السيارة: {vehicle_speed} km/h
حمل المحرك: {engine_load} %
ضغط الوقود: {fuel_pressure} kPa
'''
        
        # محاكاة رموز الأعطال
        error_codes = []
        if random.random() < 0.3:  # 30% فرصة وجود عطل
            possible_errors = ['P0300', 'P0420', 'P0171', 'P0401', 'P0128']
            error_codes = random.sample(possible_errors, random.randint(1, 2))
        
        if error_codes:
            self.error_codes_label.text = f'رموز الأعطال: {", ".join(error_codes)}'
            self.error_codes_label.color = (1, 0, 0, 1)  # أحمر
        else:
            self.error_codes_label.text = 'لا توجد رموز أعطال'
            self.error_codes_label.color = (0, 1, 0, 1)  # أخضر
    
    def clear_obd_data(self, instance):
        self.obd_data_label.text = 'اضغط "بدء المسح" لجمع بيانات السيارة\n\nسرعة المحرك: -- RPM\nدرجة الحرارة: -- °C\nسرعة السيارة: -- km/h\nحمل المحرك: -- %\nضغط الوقود: -- kPa'
        self.error_codes_label.text = 'لا توجد رموز أعطال'
        self.error_codes_label.color = (1, 1, 1, 1)

class CarDiagnosticApp(App):
    def build(self):
        self.title = 'تطبيق فحص السيارات - Car Diagnostic'
        return DiagnosticApp()

if __name__ == '__main__':
    CarDiagnosticApp().run()
      def clear_obd_data(self, instance):
        self.obd_data_label.text = 'اضغط "بدء المسح" لجمع بيانات السيارة\n\nسرعة المحرك: -- RPM\nدرجة الحرارة: -- °C\nسرعة السيارة: -- km/h\nحمل المحرك: -- %\nضغط الوقود: -- kPa'
        self.error_codes_label.text = 'لا توجد رموز أعطال'
        self.error_codes_label.color = (1, 1, 1, 1)

class CarDiagnosticApp(App):
    def build(self):
        self.title = 'تطبيق فحص السيارات - Car Diagnostic'
        return DiagnosticApp()

if __name__ == '__main__':
    CarDiagnosticApp().run()
