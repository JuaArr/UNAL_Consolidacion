import os
import flet as ft

def main(page: ft.Page) -> None:
	page.fonts = {
		"AncizarSans_Regular": "fonts/AncizarSans-Regular_02042016.otf",
		"AncizarSans_Bold": "fonts/AncizarSans-Bold_02042016.otf"
		}
	page.theme = ft.Theme(font_family = "AncizarSans_Regular") 
	page.title = "Aplicacion pija"
	page.vertical_alignment = ft.MainAxisAlignment.CENTER
	page.horizontal_alignment = ft.MainAxisAlignment.CENTER

	first_name = ft.TextField("asa")
	last_name = ft.TextField("das")
	c = ft.Column(controls=[
		first_name,
		last_name
	])
	c.disabled = True
	page.add(c, ft.Text("Título", font_family = "AncizarSans_Bold"), ft.Text("Texto de prueba"))
	# page.window.center()
	# page.window.width = 600
	# page.window.height = 400

	# def on_clicking(e):
	# 	t.value = e.path
	# 	page.update()

	# file_picker = ft.FilePicker(on_result=on_clicking)
	# page.overlay.append(file_picker)
	# but = ft.ElevatedButton("Choose directory...", on_click=lambda _: file_picker.get_directory_path())
	# t = ft.Text(color="red")
	# page.add(but)
	# page.add(t)

if __name__ == "__main__":
	os.system("cls")
	ft.app(main, assets_dir = "assets")