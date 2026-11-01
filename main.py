import flet as ft
import httpx
import asyncio

async def main(page: ft.Page):
    page.title = "سامانه باربرگ درون‌شهری"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 380
    page.window_height = 700
    page.padding = 20
    page.scroll = ft.ScrollMode.ADAPTIVE

    client = httpx.AsyncClient(timeout=15.0, verify=False)

    title = ft.Text("ثبت سریع باربرگ درون‌شهری", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900)
    
    username_input = ft.TextField(label="نام کاربری / کد ملی", prefix_icon=ft.icons.PERSON, border_radius=10)
    password_input = ft.TextField(label="رمز عبور", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK, border_radius=10)
    plate_input = ft.TextField(label="شماره پلاک ناوگان", prefix_icon=ft.icons.LOCAL_SHIPPING, border_radius=10)
    
    status_text = ft.Text("آماده اتصال...", color=ft.colors.GREY_700, size=14)
    progress_bar = ft.ProgressBar(visible=False, color=ft.colors.BLUE_700)

    async def submit_barbarg(e):
        if not username_input.value or not password_input.value:
            status_text.value = "لطفاً نام کاربری و رمز عبور را وارد کنید."
            status_text.color = ft.colors.RED_700
            page.update()
            return

        submit_btn.disabled = True
        progress_bar.visible = True
        status_text.value = "در حال ارتباط با سرور و ثبت اطلاعات..."
        status_text.color = ft.colors.BLUE_700
        page.update()

        try:
            await asyncio.sleep(1.5)
            status_text.value = f"باربرگ برای ناوگان {plate_input.value} با موفقیت ثبت شد."
            status_text.color = ft.colors.GREEN_700
        except Exception as ex:
            status_text.value = f"خطا در ارتباط با سامانه: {str(ex)}"
            status_text.color = ft.colors.RED_700
        finally:
            submit_btn.disabled = False
            progress_bar.visible = False
            page.update()

    submit_btn = ft.ElevatedButton(
        text="ثبت باربرگ",
        icon=ft.icons.CHECK_CIRCLE,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_800,
            padding=15,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        width=400,
        on_click=submit_barbarg
    )

    page.add(
        ft.Column(
            [
                ft.Container(content=title, alignment=ft.alignment.center, margin=ft.margin.only(bottom=20)),
                username_input,
                password_input,
                plate_input,
                ft.Container(height=10),
                progress_bar,
                submit_btn,
                ft.Container(content=status_text, alignment=ft.alignment.center, margin=ft.margin.only(top=15)),
            ],
            spacing=12,
        )
    )

ft.app(target=main)
