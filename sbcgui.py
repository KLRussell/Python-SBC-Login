from time import sleep
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from ctypes import windll
from ctypes import wintypes

import ctypes, pyautogui, settings

class SBCBot:
	titles = []
	name = "SBCBot"
	root = "https://osstoolbar.att.com/toolbar/index.html"

	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.enum()

	def enum(self):
		self.EnumWindows = windll.user32.EnumWindows
		self.EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
		self.GetWindowText = windll.user32.GetWindowTextW
		self.GetWindowTextLength = windll.user32.GetWindowTextLengthW
		self.IsWindowVisible = windll.user32.IsWindowVisible

	def login(self):
		self.driver = webdriver.Ie()
		print("[...] Logging in...")

		try:
			self.driver.get(self.root)

			WebDriverWait(self.driver, 30).until(
				EC.title_is("AT&T Web Toolbar")
			)

			print('\t[+] Launching SBC Toolbar.')

			ToolbarButton = WebDriverWait(self.driver, 300).until(
				EC.visibility_of_element_located((By.XPATH, "//a[@href='toolbarLaunch.html']/."))
			)

			print('\t[+] Pressing toolbar button.')

			current = self.driver.current_window_handle
			handles = self.driver.window_handles

			ToolbarButton.send_keys(Keys.ENTER)

			ToolbarButton = WebDriverWait(self.driver, 60).until(
				EC.new_window_is_opened(handles)
			)

			handles.remove(current)

			self.driver.switch_to_window(self.driver.window_handles[1])

			WebDriverWait(self.driver, 300).until(
				EC.visibility_of_element_located((By.XPATH, "//object[@name='Toolbar']"))
			)

			sleep(1)
			print('\t[+] Inputting credentials into SBC GUI menu.')

			pyautogui.typewrite(self.username)
			pyautogui.press('tab')
			pyautogui.typewrite(self.password)
			pyautogui.press('tab')
			pyautogui.press('space')

		except exceptions.ElementNotVisibleException as e:
			print('\t[-] {} Login unsuccessful.'.format(e))

	#def Verigate_Setup(self):
		#try:
			#self.driver.switch_to().window("Welcome to Enhanced Verigate! - Internet Explorer")
			#print(self.driver.title)

		#except exceptions.ElementNotVisibleException as e:
			#print('\t[-] {} Login unsuccessful.'.format(e))

	def FindWindow_Wait(self, item, secs):
		i = 0
		title = self.FindWindow(item)
		while not title and secs + 1 > i:
			sleep(1)
			i += 1
			title = self.FindWindow(item)
		return title

	def FindWindow(self, item):
		self.GetWindows()
		for title in self.titles:
			if title[1] == item:
				return title

	def FindWindowMatch(self, item):
		self.GetWindows()
		for title in self.titles:
			if item in title[1]:
				return title

	def GetWindows(self):
		self.titles = []
		self.EnumWindows(self.EnumWindowsProc(self.foreach_window), 0)

	def foreach_window(self, hwnd, lParam):
		if self.IsWindowVisible(hwnd):
			length = self.GetWindowTextLength(hwnd)
			buff = ctypes.create_unicode_buffer(length + 1)
			self.GetWindowText(hwnd, buff, length + 1)
			self.titles.append((hwnd, buff.value))
		return True

	def MaxWindow(self, hwnd):
		windll.user32.SetForegroundWindow(hwnd)
		windll.user32.SetFocus(hwnd)
		windll.user32.ShowWindow(hwnd, 3)

	def PosWindow(self, hwnd):
		win_rect = wintypes.RECT()
		windll.user32.SetForegroundWindow(hwnd)
		windll.user32.SetFocus(hwnd)
		windll.user32.ShowWindow(hwnd, 1)
		windll.user32.GetWindowRect(hwnd, ctypes.pointer(win_rect))
		windll.user32.MoveWindow(hwnd, 0, 0, win_rect.right - win_rect.left, win_rect.bottom - win_rect.top, True)

	def KillWindow(self, hwnd):
		windll.user32.SetForegroundWindow(hwnd)
		windll.user32.SetFocus(hwnd)
		windll.user32.ShowWindow(hwnd, 1)
		pyautogui.hotkey('ctrl','w')

	def KillWindow2(self, hwnd):
		self.PosWindow(hwnd)
		self.ClickGUI(400, 14)

	def ClickGUI(self, x, y):
		pyautogui.moveTo(x, y)
		pyautogui.click()

if __name__ == '__main__':
	bot = SBCBot(settings.UNAME, settings.PASS)
	title = bot.FindWindow("Toolbar")

	if title:
		print("[...] Toolbar is already launched. Checking if Verigate is opened")

		title2 = bot.FindWindowMatch("Enhanced Verigate!")

		if title2:
			print("\t[+] Verigate is already launched. Destroying Verigate Window")
			bot.KillWindow(title2[0])
			sleep(1)
	else:
		title2 = bot.FindWindowMatch("EHOSS PRODUCTION")

		if title2:
			print("[...] EHOSS PRODUCTION exists. Destroying Window")
			bot.KillWindow2(title2[0])
			sleep(1)

		title2 = bot.FindWindowMatch("AT&T Web Toolbar")

		if title2:
			print("\t[+] AT&T Web Toolbar exists. Destroying Window")
			bot.KillWindow(title2[0])
			sleep(1)

		bot.login()
		title = bot.FindWindow_Wait("Toolbar", 20)

	if title:
		print('\t[+] Login is successful.')
		print('[...] Positioning SBC flash menu for interaction.')

		bot.PosWindow(title[0])

		sleep(1)

		print('\t[+] Selecting Verification Gateway.')
		bot.ClickGUI(87, 133)
		title = bot.FindWindow_Wait("Welcome to Enhanced Verigate! - Internet Explorer", 20)
		if title:
			print('\t[+] Enhanced Verigate is launched. Maximizing window.')

			bot.MaxWindow(title[0])
			#bot.Verigate_Setup()
		else:
			print('\t[-] Selecting Verification Gateway was unsuccessful')
	else:
		print('\t[+] Login was unsuccessful. Flash menu didn''t pop up.')