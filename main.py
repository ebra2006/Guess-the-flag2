import os
import random
import requests
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

# إضافة دول جديدة للأعلام
FLAGS_DATA = {
    "Argentina": "https://flagcdn.com/w320/ar.png",
    "Australia": "https://flagcdn.com/w320/au.png",
    "South Africa": "https://flagcdn.com/w320/za.png",
    "Mexico": "https://flagcdn.com/w320/mx.png",
    "Spain": "https://flagcdn.com/w320/es.png",
    "Brazil": "https://flagcdn.com/w320/br.png",
    "Italy": "https://flagcdn.com/w320/it.png",
    "Russia": "https://flagcdn.com/w320/ru.png",
    "United Kingdom": "https://flagcdn.com/w320/gb.png",
    "Germany": "https://flagcdn.com/w320/de.png",
    "India": "https://flagcdn.com/w320/in.png",
    "France": "https://flagcdn.com/w320/fr.png",
    "Canada": "https://flagcdn.com/w320/ca.png",
    "Japan": "https://flagcdn.com/w320/jp.png",
    "China": "https://flagcdn.com/w320/cn.png",
    "Turkey": "https://flagcdn.com/w320/tr.png",
    "Saudi Arabia": "https://flagcdn.com/w320/sa.png",
    "Greece": "https://flagcdn.com/w320/gr.png",
    "United States": "https://flagcdn.com/w320/us.png",  # إضافة الولايات المتحدة
    "South Korea": "https://flagcdn.com/w320/kr.png",  # إضافة كوريا الجنوبية
    "Nigeria": "https://flagcdn.com/w320/ng.png",  # إضافة نيجيريا
    "Pakistan": "https://flagcdn.com/w320/pk.png",  # إضافة باكستان
    "Thailand": "https://flagcdn.com/w320/th.png",  # إضافة تايلاند
    "Sweden": "https://flagcdn.com/w320/se.png",  # إضافة السويد
    "Norway": "https://flagcdn.com/w320/no.png",  # إضافة النرويج
    "Denmark": "https://flagcdn.com/w320/dk.png",  # إضافة الدنمارك
     "United Arab Emirates": "https://flagcdn.com/w320/ae.png",  # الإمارات العربية المتحدة
    "Jordan": "https://flagcdn.com/w320/jo.png",  # الأردن
    "Kuwait": "https://flagcdn.com/w320/kw.png",  # الكويت
    "Lebanon": "https://flagcdn.com/w320/lb.png",  # لبنان
    "Syria": "https://flagcdn.com/w320/sy.png",  # سوريا
    "Iraq": "https://flagcdn.com/w320/iq.png",  # العراق
    "Oman": "https://flagcdn.com/w320/om.png",  # عمان
    "Palestine": "https://flagcdn.com/w320/ps.png",  # فلسطين
    "Qatar": "https://flagcdn.com/w320/qa.png",  # قطر
    "Bahrain": "https://flagcdn.com/w320/bh.png",  # البحرين
    "Yemen": "https://flagcdn.com/w320/ye.png",  # اليمن
    "Morocco": "https://flagcdn.com/w320/ma.png",  # المغرب
    "Tunisia": "https://flagcdn.com/w320/tn.png",  # تونس
    "Algeria": "https://flagcdn.com/w320/dz.png",  # الجزائر
    "Libya": "https://flagcdn.com/w320/ly.png",  # ليبيا
    "Sudan": "https://flagcdn.com/w320/sd.png",  # السودان
    "Mauritania": "https://flagcdn.com/w320/mr.png",  # موريتانيا
    "Somalia": "https://flagcdn.com/w320/so.png"  # الصومال
    
}

if not os.path.exists("flags"):
    os.makedirs("flags")

# تحميل الأعلام والتأكد من تسميتها بشكل صحيح
for country, url in FLAGS_DATA.items():
    path = os.path.join("flags", f"{country.lower().replace(' ', '_')}.png")
    if not os.path.exists(path):
        try:
            response = requests.get(url)
            with open(path, "wb") as f:
                f.write(response.content)
        except:
            print(f"فشل تحميل علم {country}")

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)

        title = Label(text="🌍 Guess The Flag 🌍", font_size=36, size_hint=(1, 0.3), color=(1, 1, 1, 1))
        layout.add_widget(title)
        btn_timer = Button(text="Play with Timer", font_size=24, size_hint=(1, 0.2), background_normal='', background_color=(0.2, 0.6, 0.8, 1), border=(10, 10, 10, 10))
        btn_timer.bind(on_press=self.start_with_timer)

        btn_no_timer = Button(text="Play without Timer", font_size=24, size_hint=(1, 0.2), background_normal='', background_color=(0.3, 0.7, 0.3, 1), border=(10, 10, 10, 10))
        btn_no_timer.bind(on_press=self.start_without_timer)

        layout.add_widget(btn_timer)
        layout.add_widget(btn_no_timer)

        with layout.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def start_with_timer(self, instance):
        self.manager.get_screen("game").play_with_timer = True
        self.manager.get_screen("game").start_game()
        self.manager.current = "game"

    def start_without_timer(self, instance):
        self.manager.get_screen("game").play_with_timer = False
        self.manager.get_screen("game").start_game()
        self.manager.current = "game"


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.play_with_timer = False
        self.score = 0
        self.timer_event = None
        self.questions_used = []  # لتخزين الأسئلة التي تم عرضها

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        with self.layout.canvas.before:
            Color(0.05, 0.05, 0.05, 1)  # خلفية سوداء ناعمة
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self._update_rect, pos=self._update_rect)

        self.title_label = Label(text="What Flag is This?", font_size=32, color=(1, 1, 1, 1), size_hint=(1, 0.1))
        self.score_label = Label(text=f"Score: {self.score}", font_size=24, color=(1, 1, 1, 1), size_hint=(1, 0.1))
        self.timer_label = Label(text="", font_size=20, size_hint=(1, 0.1), color=(1, 0.3, 0.3, 1))

        self.flag_image = Image(size_hint=(None, None), size=(400, 200))  # تم زيادة حجم العلم ليكون أكثر وضوحًا
        self.flag_image.size_hint = (None, None)
        self.flag_image.width = 400
        self.flag_image.height = 200
        self.flag_image.pos_hint = {"center_x": 0.5}  # تمركز العلم في المنتصف

        self.buttons_layout = GridLayout(cols=2, spacing=15, size_hint=(1, 0.3))

        # زر العودة إلى الصفحة الرئيسية
        self.back_button = Button(text="Back to Start", size_hint=(1, 0.1), background_normal='', background_color=(0.6, 0.3, 0.8, 1), border=(10, 10, 10, 10))
        self.back_button.bind(on_press=self.back_to_start)

        # زر الخروج من اللعبة
        self.exit_button = Button(text="Exit Game", size_hint=(1, 0.1), background_normal='', background_color=(0.8, 0.3, 0.3, 1), border=(10, 10, 10, 10))
        self.exit_button.bind(on_press=self.exit_game)

        # إضافة كل العناصر إلى layout
        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.score_label)
        self.layout.add_widget(self.timer_label)
        self.layout.add_widget(self.flag_image)

        # مسافة بين الأزرار وصورة العلم
        self.layout.add_widget(Label(size_hint=(1, 0.1)))  # مسافة بين العلم والأزرار

        self.layout.add_widget(self.buttons_layout)

        # استخدام BoxLayout لترتيب الأزرار في الأسفل بشكل منفصل
        bottom_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, 0.1))
        bottom_layout.add_widget(self.back_button)
        bottom_layout.add_widget(self.exit_button)

        self.layout.add_widget(bottom_layout)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def start_game(self):
        self.score = 0
        self.update_score()
        self.questions_used = []  # إعادة تعيين الأسئلة المستخدمة
        self.generate_question()

    def update_timer(self, dt):
        self.time_left -= 1
        self.timer_label.text = f"⏰ Time Left: {self.time_left}s"
        if self.time_left <= 0:
            Clock.unschedule(self.timer_event)
            self.show_popup("Game Over", f"You ran out of time! The correct answer was: {self.correct_country}")
            self.disable_buttons()
            Clock.schedule_once(self.goto_start_screen, 2)  # الانتقال إلى الشاشة الرئيسية بعد 2 ثانية

    def goto_start_screen(self, dt):
        self.manager.current = "start"  # العودة إلى الشاشة الرئيسية

    def generate_question(self):
        if self.timer_event:
            Clock.unschedule(self.timer_event)

        self.buttons_layout.clear_widgets()
        countries = list(FLAGS_DATA.keys())

        # إذا تم عرض جميع الأسئلة
        if len(self.questions_used) == len(countries):
            self.questions_used = []  # إعادة تعيين الأسئلة المستخدمة
            self.show_popup("لقد ربحت!", "لقد أجبت على جميع الأسئلة بنجاح!")
            self.start_game()

        # اختيار دولة جديدة لم يتم استخدامها
        available_countries = list(set(countries) - set(self.questions_used))
        self.correct_country = random.choice(available_countries)
        self.questions_used.append(self.correct_country)  # إضافة السؤال الذي تم استخدامه

        correct_path = os.path.join("flags", f"{self.correct_country.lower().replace(' ', '_')}.png")
        self.flag_image.source = correct_path

        # ضبط حجم الأعلام ليكون ثابتًا
        self.flag_image.size_hint = (None, None)
        self.flag_image.width = 400  # زيادة الحجم قليلاً
        self.flag_image.height = 200  # زيادة الحجم قليلاً

        options = set([self.correct_country])
        while len(options) < 4:
            choice = random.choice(countries)
            options.add(choice)

        options = list(options)
        random.shuffle(options)

        self.buttons = []
        for option in options:
            button = Button(text=option, size_hint=(1, None), height=70, font_size=18,
                            background_normal='', background_color=(0.4, 0.8, 1, 1), color=(1, 1, 1, 1), border=(10, 10, 10, 10))
            button.bind(on_press=self.check_answer)
            self.buttons_layout.add_widget(button)
            self.buttons.append(button)

        if self.play_with_timer:
            self.time_left = 5
            self.timer_label.text = f"⏰ Time Left: {self.time_left}s"
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)
        else:
            self.timer_label.text = ""

    def check_answer(self, instance):
        selected_country = instance.text
        if selected_country == self.correct_country:
            self.score += 1
            instance.background_color = (0, 0.7, 0, 1)  # الإجابة الصحيحة تصبح خضراء
        else:
            instance.background_color = (0.8, 0, 0, 1)  # الإجابة الخاطئة تصبح حمراء

        self.update_score()
        self.disable_buttons()

        # الانتقال إلى السؤال التالي بشكل تلقائي بعد إجابة اللاعب
        Clock.schedule_once(lambda dt: self.generate_question(), 1)

    def disable_buttons(self):
        for button in self.buttons:
            button.disabled = True

    def update_score(self):
        self.score_label.text = f"Score: {self.score}"

    def show_popup(self, title, message):
        popup = ModalView(size_hint=(0.8, 0.4), background_color=(0, 0, 0, 0.8))
        box = BoxLayout(orientation='vertical', spacing=10, padding=20)
        box.add_widget(Label(text=title, font_size=28, color=(1, 0.8, 0.2, 1)))
        box.add_widget(Label(text=message, font_size=20, color=(1, 1, 1, 1)))
        popup.add_widget(box)
        popup.auto_dismiss = True
        popup.open()

    def exit_game(self, instance):
        App.get_running_app().stop()

    def back_to_start(self, instance):
        self.manager.current = "start"  # التبديل إلى الشاشة الرئيسية


class GuessTheFlagApp(App):
    def build(self):
        self.manager = ScreenManager(transition=FadeTransition())
        self.manager.add_widget(StartScreen(name="start"))
        self.manager.add_widget(GameScreen(name="game"))
        return self.manager


if __name__ == "__main__":
    GuessTheFlagApp().run()
