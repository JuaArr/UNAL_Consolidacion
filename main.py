import os
import flet as ft

def main(page: ft.Page) -> None:
	page.window.center()
	page.window.width = 600
	page.window.height = 400

	def on_clicking(e):
		t.value = e.path
		page.update()

	file_picker = ft.FilePicker(on_result=on_clicking)
	page.overlay.append(file_picker)
	but = ft.ElevatedButton("Choose directory...", on_click=lambda _: file_picker.get_directory_path())
	t = ft.Text(color="red")
	page.add(but)
	page.add(t)

if __name__ == "__main__":
	os.system("cls")
	ft.app(main)