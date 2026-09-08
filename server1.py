import colorsys
import math
import os
import platform
import random
import time
import unicodedata
from typing import List, Optional, Tuple

from rich import box
from rich.color import Color
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.style import Style
from rich.text import Text


class LinuxLogoGlitchV3:
    PHRASE = "Linux by Nguyễn Tấn Dũng"

    LOGO_LINES = [
        "⠀⠻⣿⣿⣿⠟⠛⢿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   Admin  : Nguyễn Tấn Dũng",
        "⠀⠀⣿⣿⣷⠀⠀⠈⣠⣾⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀            MinhAnhs",
        "⠀⠀⣿⣿⡇⠀⠀⠀⣿⣿⣿⠀⣰⣾⣠⣴⣿⣠⣶⡶⠀⣤⡶⠒⣶⣶⠀⣾⡟⠙⠓⠀   Server : Online",
        "⠀⠀⣿⣿⣿⠀⠀⠀⣾⣿⡟⣰⣿⡟⠀⣿⠏⣸⣿⠃⣾⡟⠀⣴⣿⠃⠀⠻⢿⣶⣄⠀   Time   : thoigian",
        "⠀⣴⣿⣿⠋⣀⣴⣿⡿⢏⠔⣽⠿⠀⠾⠟⠀⠿⠿⠖⠿⠷⠊⠹⠿⠖⢤⣤⣤⣿⡿⠀   From   : vitri",
        "⠼⠿⠿⠿⠟⠛⠛⠉⠀Linux by Nguyễn Tấn Dũng",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    ]

    GLITCH_CHARS = "!<>-_/[]{}=+*^?#@$%&░▒▓█"

    # Nền xám vừa, không quá chói (Dạng tuple RGB thuần)
    GRAY_BG_RGB = (50, 50, 50)
    GRAY_BG = Color.from_rgb(*GRAY_BG_RGB)

    # Số điểm màu trong gradient
    PALETTE_SIZE = 5

    def __init__(
        self,
        fps: int = 60,
        glitch_duration: float = 2.8,
        palette_speed: float = 2.6,
        palette_min_interval: float = 2.2,
        palette_max_interval: float = 4.8,
    ) -> None:
        self.console = Console(highlight=False)

        self.fps = max(20, int(fps))
        self.glitch_duration = max(0.2, float(glitch_duration))
        self.palette_speed = float(palette_speed)

        self.palette_interval = (
            float(palette_min_interval),
            float(palette_max_interval),
        )

        # Chuẩn hóa Unicode
        self.logo_lines: List[str] = [
            unicodedata.normalize("NFC", line) for line in self.LOGO_LINES
        ]
        self.phrase: str = unicodedata.normalize("NFC", self.PHRASE)

        self._precompute_positions()

        # Palette ban đầu ngẫu nhiên
        self._current_palette: List[Tuple[int, int, int]] = self._random_palette()
        self._target_palette: List[Tuple[int, int, int]] = list(self._current_palette)
        self._next_palette_time: float = time.perf_counter() + random.uniform(
            *self.palette_interval
        )

    def _precompute_positions(self) -> None:
        self.line_offsets: List[int] = []
        offset = 0

        for line in self.logo_lines:
            self.line_offsets.append(offset)
            offset += len(line)

        self.total_chars = max(1, offset)
        self.phrase_pos: Optional[Tuple[int, int, int]] = None

        for line_index, line in enumerate(self.logo_lines):
            found = line.find(self.phrase)
            if found != -1:
                self.phrase_pos = (line_index, found, found + len(self.phrase))
                break

    def clear_screen(self) -> None:
        system = platform.system().lower()

        if system == "windows":
            command = "cls"
        elif system == "linux":
            command = "clear"
        else:
            self.console.clear()
            return

        try:
            if os.system(command) != 0:
                self.console.clear()
        except Exception:
            self.console.clear()

    @staticmethod
    def _clamp01(value: float) -> float:
        return max(0.0, min(1.0, value))

    @staticmethod
    def _hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
        h = h % 1.0
        s = max(0.0, min(1.0, s))
        v = max(0.0, min(1.0, v))

        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return round(r * 255), round(g * 255), round(b * 255)

    @staticmethod
    def _mix_rgb(
        color_a: Tuple[int, int, int],
        color_b: Tuple[int, int, int],
        factor: float,
    ) -> Tuple[int, int, int]:
        factor = max(0.0, min(1.0, factor))

        return (
            round(color_a[0] + (color_b[0] - color_a[0]) * factor),
            round(color_a[1] + (color_b[1] - color_a[1]) * factor),
            round(color_a[2] + (color_b[2] - color_a[2]) * factor),
        )

    def _random_palette(self) -> List[Tuple[int, int, int]]:
        base_hue = random.random()
        spread = random.uniform(0.14, 0.40)
        base_sat = random.uniform(0.58, 0.84)

        palette: List[Tuple[int, int, int]] = []
        white_rgb = (255, 255, 255)

        for i in range(self.PALETTE_SIZE):
            ratio = i / max(1, self.PALETTE_SIZE - 1)
            hue_offset = -spread / 2.0 + spread * ratio
            hue = base_hue + hue_offset + random.uniform(-0.015, 0.015)

            sat = base_sat + random.uniform(-0.08, 0.08)
            sat = max(0.48, min(0.92, sat))

            val = random.uniform(0.97, 1.0)
            rgb = self._hsv_to_rgb(hue, sat, val)

            # Trộn thêm trắng để màu sáng/pastel hơn
            rgb = self._mix_rgb(rgb, white_rgb, random.uniform(0.14, 0.26))
            palette.append(rgb)

        return palette

    def _update_palette(self, now: float, dt: float) -> None:
        if now >= self._next_palette_time:
            self._target_palette = self._random_palette()
            self._next_palette_time = now + random.uniform(*self.palette_interval)

        factor = 1.0 - math.exp(-dt * self.palette_speed)

        for i in range(self.PALETTE_SIZE):
            self._current_palette[i] = self._mix_rgb(
                self._current_palette[i],
                self._target_palette[i],
                factor,
            )

    @staticmethod
    def _smoothstep(x: float) -> float:
        x = max(0.0, min(1.0, x))
        return x * x * (3.0 - 2.0 * x)

    def _gradient_rgb(self, t: float, now: float) -> Tuple[int, int, int]:
        t = self._clamp01(float(t))

        shift = 0.05 * math.sin(now * 0.75)
        wave = 0.016 * math.sin(now * 1.35 + t * (2.0 * math.pi))

        t = self._clamp01(t + shift + wave)
        stops = self._current_palette

        if len(stops) == 1:
            return stops[0]

        segments = len(stops) - 1
        scaled = t * segments
        index = min(int(scaled), segments - 1)
        local_t = scaled - index

        return self._mix_rgb(stops[index], stops[index + 1], local_t)

    def _gradient_color(self, t: float, now: float) -> Color:
        return Color.from_rgb(*self._gradient_rgb(t, now))

    def _char_t(self, line_index: int, char_index: int) -> float:
        if self.total_chars <= 1:
            return 0.0

        global_index = self.line_offsets[line_index] + char_index
        return global_index / (self.total_chars - 1)

    def _phrase_style(self, line_index: int, start: int, end: int, now: float) -> Style:
        middle = start + (end - start) // 2
        rgb = self._gradient_rgb(self._char_t(line_index, middle), now)

        # Làm sáng thêm bằng cách trộn với trắng (75, 75, 75)
        rgb = self._mix_rgb(rgb, (255, 255, 255), 0.34)

        return Style(
            color=Color.from_rgb(*rgb),
            bgcolor=self.GRAY_BG,
            italic=True,
        )

    def _glitch_line(self, line: str, line_index: int, intensity: float) -> str:
        if intensity <= 0.0 or not line:
            return line

        chars = list(line)
        phrase_line, phrase_start, phrase_end = (-1, -1, -1)
        if self.phrase_pos is not None:
            phrase_line, phrase_start, phrase_end = self.phrase_pos

        for idx, char in enumerate(chars):
            if line_index == phrase_line and phrase_start <= idx < phrase_end:
                continue

            probability = intensity

            if char == " " or char == "\u2800" or char.isspace():
                probability *= 0.22

            if random.random() < probability:
                chars[idx] = random.choice(self.GLITCH_CHARS)

        return "".join(chars)

    def _build_text(self, lines: List[str], now: float) -> Text:
        text = Text(no_wrap=True, overflow="ignore")
        phrase_line = -1
        phrase_start = -1
        phrase_end = -1

        if self.phrase_pos is not None:
            phrase_line, phrase_start, phrase_end = self.phrase_pos

        for line_index, line in enumerate(lines):
            if line_index == phrase_line and phrase_start >= 0:
                before = line[:phrase_start]
                phrase = line[phrase_start:phrase_end]
                after = line[phrase_end:]

                for char_index, char in enumerate(before):
                    text.append(
                        char,
                        Style(
                            color=self._gradient_color(
                                self._char_t(line_index, char_index),
                                now,
                            )
                        ),
                    )

                if phrase:
                    text.append(
                        phrase,
                        self._phrase_style(line_index, phrase_start, phrase_end, now),
                    )

                for offset_index, char in enumerate(after):
                    char_index = phrase_end + offset_index
                    text.append(
                        char,
                        Style(
                            color=self._gradient_color(
                                self._char_t(line_index, char_index),
                                now,
                            )
                        ),
                    )
            else:
                for char_index, char in enumerate(line):
                    text.append(
                        char,
                        Style(
                            color=self._gradient_color(
                                self._char_t(line_index, char_index),
                                now,
                            )
                        ),
                    )

            if line_index != len(lines) - 1:
                text.append("\n")

        return text

    def _build_panel(self, lines: List[str], now: float) -> Panel:
        border_t = (now * 0.22) % 1.0
        border_rgb = self._gradient_rgb(border_t, now)
        border_style = Style(color=Color.from_rgb(*border_rgb))

        content = self._build_text(lines, now)

        return Panel(
            content,
            box=box.ROUNDED,
            border_style=border_style,
            padding=(1, 2),
            expand=False,
        )

    def run(self) -> None:
        """
        Chạy animation và dừng ngay khi hết hiệu ứng glitch.
        """
        self.clear_screen()

        try:
            self.console.show_cursor(False)
        except Exception:
            pass

        start = time.perf_counter()
        last = start

        self._next_palette_time = start + random.uniform(*self.palette_interval)

        frame_interval = 1.0 / self.fps
        next_frame = start

        current_intensity = 0.0
        target_intensity = 0.0
        last_target_switch = 0.0

        try:
            with Live(
                self._build_panel(self.logo_lines, start),
                console=self.console,
                auto_refresh=False,
                refresh_per_second=self.fps,
                screen=False,
                transient=False,
            ) as live:
                live.refresh()

                while True:
                    now = time.perf_counter()
                    elapsed = now - start
                    dt = max(0.0001, now - last)
                    last = now

                    self._update_palette(now, dt)

                    # Nếu đã chạy xong hiệu ứng glitch thì render frame gốc rồi dừng ngay
                    if elapsed >= self.glitch_duration:
                        live.update(self._build_panel(self.logo_lines, now))
                        live.refresh()
                        break

                    progress = min(1.0, elapsed / self.glitch_duration)
                    envelope = 1.0 - self._smoothstep(progress)

                    if now - last_target_switch >= random.uniform(0.035, 0.10):
                        target_intensity = envelope * random.uniform(0.06, 0.42)
                        last_target_switch = now

                    intensity_smooth_factor = 1.0 - math.exp(-dt * 26.0)
                    current_intensity += (
                        target_intensity - current_intensity
                    ) * intensity_smooth_factor

                    if current_intensity < 0.001:
                        current_intensity = 0.0

                    if current_intensity > 0.0:
                        render_lines = [
                            self._glitch_line(line, line_index, current_intensity)
                            for line_index, line in enumerate(self.logo_lines)
                        ]
                    else:
                        render_lines = self.logo_lines

                    live.update(self._build_panel(render_lines, now))
                    live.refresh()

                    next_frame += frame_interval
                    if next_frame < time.perf_counter():
                        next_frame = time.perf_counter() + frame_interval

                    sleep_time = max(0.0, next_frame - time.perf_counter())
                    if sleep_time > 0:
                        time.sleep(sleep_time)

        except KeyboardInterrupt:
            pass
        finally:
            try:
                self.console.show_cursor(True)
            except Exception:
                pass


if __name__ == "__main__":
    LinuxLogoGlitchV3(
        fps=80,
        glitch_duration=1.5,
        palette_speed=9.5,
        palette_min_interval=0.9,
        palette_max_interval=1.5,
    ).run()
