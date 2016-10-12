'''
Created on Oct 11, 2016

@author: ASUS
'''

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from main import NQueens
import numpy


class StartScreen(Screen):

	def __init__(self, **kwargs):
		super(StartScreen, self).__init__(**kwargs)
		layout = BoxLayout(padding=10, orientation='vertical')
		sub_layout = BoxLayout()
		self.label = Label(text='Number of Queens')
		self.N = TextInput(multiline=False)
		sub_layout.add_widget(self.label)
		sub_layout.add_widget(self.N)
		layout.add_widget(sub_layout)
		btn_start = Button(text='Start')
		btn_start.bind(on_press=self.startGame)
		layout.add_widget(btn_start)
		self.add_widget(layout)

	def startGame(self, btn):
		txt = self.N.text.strip()
		if txt.isdigit():
			self.manager.get_screen('board_screen').setN(int(txt))
			self.manager.get_screen('board_screen').reshape()
			len_sol = len(self.manager.get_screen('board_screen').solution)
			if len_sol > 0:
				self.manager.current = 'board_screen'
			else:
				self.manager.current = 'no_answer_screen'

	def reshape(self):
		self.N.text = ''


class BoardScreen(Screen):
	
	def __init__(self, **kwargs):
		super(BoardScreen, self).__init__(**kwargs)
		


	def reshape(self):
		self.clear_widgets()
		self.buttons = []
		self.playable = True
		self.state = [0 for i in range(self.N**2)]
		
		self.find_solution()

		if len(self.solution) > 0:
			brd_lay = GridLayout(cols=self.N)
			for i in range(1,self.N**2+1):
				button_i = Button(text='', font_size=24)
				button_i.bind(on_press=self.board_click)
				self.buttons.append(button_i)
				brd_lay.add_widget(button_i)

			btn_lay = BoxLayout(padding=10, orientation='vertical', size_hint_x=None, width=150)
			self.btn_check = Button(text='Check')
			self.btn_check.bind(on_press=self.check_answer)
			self.btn_show = Button(text='Show Answer')
			self.btn_show.bind(on_press=self.show_answer)
			self.btn_restart = Button(text='Restart')
			self.btn_restart.bind(on_press=self.restart)
			btn_lay.add_widget(self.btn_check)
			btn_lay.add_widget(self.btn_show)
			btn_lay.add_widget(self.btn_restart)

			screen_lay = GridLayout(cols=2, padding=10)
			screen_lay.add_widget(brd_lay)
			screen_lay.add_widget(btn_lay)

			self.add_widget(screen_lay)			


	def find_solution(self):
		prob = NQueens(self.N)
	    	prob.row_constraint_init()
	    	prob.column_constraint_init()
	    	prob.diagonal_constraint_init()
	    	prob.write_sat_input()
    		prob.run_minisat("input.in", "output.out")
    		self.problem = prob
    		self.solution = prob.get_output()


	def setN(self, N):
		self.N = N
		self.posses = N


	def board_click(self, btn):
		if self.playable:
			index = self.buttons.index(btn)
			if btn.text == '':
				if self.posses > 0:
					self.posses -= 1
					btn.text = 'Q'
					self.state[index] = 1
			else:
				self.posses += 1
				btn.text = ''
				self.state[index] = 0


	def check_answer(self, btn):
		if self.playable:
			chunk = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
			chunked = chunk(self.state, self.N)
			np = numpy.array(chunked)
			if self.problem.valid_answer(np):
				self.manager.current = 'win_screen'
			else:
				self.manager.current = 'wrong_ans_screen'


	def show_answer(self, btn):
		self.playable = False
		for item in self.buttons:
			item.text = ''

		for ii in range(len(self.solution)):
			if self.solution[ii] > 0:
				self.buttons[ii].text = 'Q'


	def restart(self, btn):
		self.manager.get_screen('start_screen').reshape()
		self.manager.current = 'start_screen'



class Notif_1_Screen(Screen):
	def __init__(self, msg, **kwargs):
		super(Notif_1_Screen, self).__init__(**kwargs)
		layout = BoxLayout(padding=10, orientation='vertical')
		lbl = Label(text=msg)
		btn = Button(text='Restart')
		btn.bind(on_press=self.restart)
		layout.add_widget(lbl)
		layout.add_widget(btn)
		self.add_widget(layout)

	def restart(self, btn):
		self.manager.get_screen('start_screen').reshape()
		self.manager.current = 'start_screen'


class Notif_2_Screen(Screen):
	def __init__(self, **kwargs):
		super(Notif_2_Screen, self).__init__(**kwargs)
		layout = BoxLayout(padding=10, orientation='vertical')
		lbl = Label(text='Jawaban Anda belum benar :(')
		btn_back = Button(text='Back')
		btn_back.bind(on_press=self.back)
		btn_restart = Button(text='Restart')
		btn_restart.bind(on_press=self.restart)
		layout.add_widget(lbl)
		layout.add_widget(btn_back)
		layout.add_widget(btn_restart)
		self.add_widget(layout)

	def restart(self, btn):
		self.manager.get_screen('start_screen').reshape()
		self.manager.current = 'start_screen'

	def back(self, btn):
		self.manager.current = 'board_screen'


sm = ScreenManager()
sm.add_widget(StartScreen(name='start_screen'))
sm.add_widget(BoardScreen(name='board_screen'))
sm.add_widget(Notif_1_Screen(name='no_answer_screen', msg='Tidak ada jawaban untuk ukuran ini'))
sm.add_widget(Notif_1_Screen(name='win_screen', msg='Selamat, Anda menang :)'))
sm.add_widget(Notif_2_Screen(name='wrong_ans_screen'))


class Play(App):

	def build(self):
		return sm


if __name__ == '__main__':
	Play().run()