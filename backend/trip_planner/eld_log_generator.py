
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
from typing import List, Dict
import io
import base64


class ELDLogGenerator:
    

    
    WIDTH = 1400
    HEIGHT = 860

    
    COLOR_BG        = '#020810'   
    COLOR_BG2       = '#071220'   
    COLOR_GRID      = '#0c2a3a'   
    COLOR_GRID_HOT  = '#0a3d52'   
    COLOR_TEXT      = '#c8e8f8'   
    COLOR_MUTED     = '#2e6a86'   
    COLOR_ACCENT    = '#00d4ff'   

    
    COLOR_OFFDUTY   = '#1a3a4a'   
    COLOR_SLEEPER   = '#0a2a60'   
    COLOR_DRIVING   = '#cc1a2e'   
    COLOR_ONDUTY    = '#b87000'   

    
    GLOW_OFFDUTY    = '#2a5a70'
    GLOW_SLEEPER    = '#1040a0'
    GLOW_DRIVING    = '#ff2040'
    GLOW_ONDUTY     = '#ffaa00'

    
    GRID_START_Y = 230
    GRID_HEIGHT  = 360
    GRID_START_X = 130
    GRID_WIDTH   = 1180
    HOURS_IN_DAY = 24

    
    STATUS_MAP = {
        'off_duty': {'label': 'OFF DUTY',            'color': COLOR_DRIVING,   'glow': GLOW_OFFDUTY,   'y_position': 0},
        'sleeper':  {'label': 'SLEEPER BERTH',       'color': COLOR_SLEEPER,   'glow': GLOW_SLEEPER,  'y_position': 1},
        'driving':  {'label': 'DRIVING',             'color': COLOR_DRIVING,   'glow': GLOW_DRIVING,  'y_position': 2},
        'on_duty':  {'label': 'ON DUTY (Not Driving)','color': COLOR_ONDUTY,   'glow': GLOW_ONDUTY,   'y_position': 3},
    }

    
    STATUS_MAP['off_duty']['color'] = COLOR_OFFDUTY
    STATUS_MAP['sleeper']['color']  = COLOR_SLEEPER

    def __init__(self):
        self.font_title   = None
        self.font_orb     = None   
        self.font_regular = None
        self.font_small   = None
        self.font_tiny    = None

    
    def _get_fonts(self):
        
        deja_bold   = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
        deja_reg    = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
        deja_sans   = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        deja_sb     = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        try:
            self.font_title   = ImageFont.truetype(deja_bold, 26)
            self.font_orb     = ImageFont.truetype(deja_bold, 14)
            self.font_regular = ImageFont.truetype(deja_sans,  15)
            self.font_small   = ImageFont.truetype(deja_sans,  12)
            self.font_tiny    = ImageFont.truetype(deja_sans,  10)
        except Exception:
            default = ImageFont.load_default()
            self.font_title = self.font_orb = self.font_regular = \
                self.font_small = self.font_tiny = default

    
    @staticmethod
    def _hex(h: str):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def _draw_rect_glow(self, draw: ImageDraw.Draw,
                        x0, y0, x1, y1,
                        fill: str, glow: str,
                        radius: int = 3):
        
        draw.rectangle([x0, y0, x1, y1], fill=fill)
        
        draw.line([(x0, y0), (x1, y0)], fill=glow, width=2)
        
        draw.line([(x0, y1), (x1, y1)], fill=glow, width=1)

    
    def generate_daily_log(
        self,
        day_number: int,
        schedule_segments: List[Dict],
        driver_name: str = "Driver",
        date: str = None,
    ) -> str:
        self._get_fonts()

        img  = Image.new('RGB', (self.WIDTH, self.HEIGHT), self.COLOR_BG)
        draw = ImageDraw.Draw(img)

        self._draw_background(draw)
        self._draw_header(draw, day_number, driver_name, date)
        self._draw_grid(draw)
        self._draw_status_graph(draw, schedule_segments)
        self._draw_summary(draw, schedule_segments)

        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}"

    
    def _draw_background(self, draw: ImageDraw.Draw):
        
        
        for y in range(0, self.HEIGHT, 4):
            draw.line([(0, y), (self.WIDTH, y)],
                      fill='#050e18', width=1)

        
        for x in range(0, self.WIDTH, 48):
            for y in range(0, self.HEIGHT, 48):
                draw.rectangle([x-1, y-1, x+1, y+1], fill='#0a2030')

        
        for i in range(3):
            alpha = 80 - i * 25
            draw.rectangle(
                [0, i, self.WIDTH, i + 1],
                fill='#00d4ff'
            )

        
        draw.rectangle([0, self.HEIGHT - 2, self.WIDTH, self.HEIGHT],
                       fill='#00d4ff')

        
        sz = 18
        c  = '#00d4ff'
        corners = [
            (4, 4), (self.WIDTH - 4 - sz, 4),
            (4, self.HEIGHT - 4 - sz), (self.WIDTH - 4 - sz, self.HEIGHT - 4 - sz),
        ]
        for (cx, cy) in corners:
            draw.rectangle([cx, cy, cx + sz, cy + 2], fill=c)
            draw.rectangle([cx, cy, cx + 2, cy + sz], fill=c)
            draw.rectangle([cx + sz - 2, cy, cx + sz, cy + sz], fill=c)
            draw.rectangle([cx, cy + sz - 2, cx + sz, cy + sz], fill=c)

    
    def _draw_header(self, draw: ImageDraw.Draw,
                     day_number: int, driver_name: str, date: str):
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        
        title = f"ELD DAILY LOG  //  DAY {day_number:02d}"
        draw.text((self.GRID_START_X, 24), title,
                  fill=self.COLOR_ACCENT, font=self.font_title)

        
        draw.text((self.GRID_START_X, 62),
                  f"DRIVER: {driver_name.upper()}",
                  fill=self.COLOR_TEXT, font=self.font_orb)
        draw.text((self.GRID_START_X, 82),
                  f"DATE  : {date}",
                  fill=self.COLOR_MUTED, font=self.font_orb)

        
        draw.rectangle([self.GRID_START_X, 106,
                        self.GRID_START_X + self.GRID_WIDTH, 107],
                       fill='#0a3d52')

        
        lx = self.WIDTH - 310
        ly = 24
        draw.text((lx, ly - 2), "STATUS LEGEND",
                  fill=self.COLOR_ACCENT, font=self.font_orb)
        ly += 18
        for key, info in self.STATUS_MAP.items():
            
            draw.rectangle([lx, ly + 2, lx + 22, ly + 14],
                           fill=info['color'])
            draw.rectangle([lx, ly + 2, lx + 22, ly + 4],
                           fill=info['glow'])
            draw.text((lx + 28, ly), info['label'],
                      fill=self.COLOR_TEXT, font=self.font_small)
            ly += 22

    
    def _draw_grid(self, draw: ImageDraw.Draw):
        px_per_hr = self.GRID_WIDTH / self.HOURS_IN_DAY
        row_h     = self.GRID_HEIGHT // 4
        labels    = ['OFF\nDUTY', 'SLEEPER\nBERTH', 'DRIVING', 'ON DUTY\nNOT DRV']

        
        row_fills = ['#040e18', '#050f1c', '#04101e', '#04111f']
        for i in range(4):
            y0 = self.GRID_START_Y + i * row_h
            draw.rectangle(
                [self.GRID_START_X, y0,
                 self.GRID_START_X + self.GRID_WIDTH, y0 + row_h],
                fill=row_fills[i]
            )

        
        for i in range(5):
            y = self.GRID_START_Y + i * row_h
            col = self.COLOR_ACCENT if i == 0 or i == 4 else self.COLOR_GRID_HOT
            draw.line(
                [(self.GRID_START_X, y),
                 (self.GRID_START_X + self.GRID_WIDTH, y)],
                fill=col, width=1
            )

        
        for i in range(self.HOURS_IN_DAY + 1):
            x   = self.GRID_START_X + int(i * px_per_hr)
            hot = (i % 6 == 0)
            draw.line(
                [(x, self.GRID_START_Y),
                 (x, self.GRID_START_Y + self.GRID_HEIGHT)],
                fill=self.COLOR_GRID_HOT if hot else self.COLOR_GRID,
                width=2 if hot else 1
            )
            if i % 2 == 0:
                label = f"{i:02d}"
                y_lbl = self.GRID_START_Y + self.GRID_HEIGHT + 8
                draw.text((x - 10, y_lbl), label,
                          fill=self.COLOR_ACCENT if hot else self.COLOR_MUTED,
                          font=self.font_small)

        
        draw.text((self.GRID_START_X - 4,
                   self.GRID_START_Y + self.GRID_HEIGHT + 8),
                  "HR", fill=self.COLOR_MUTED, font=self.font_tiny)

        
        short = ['OFF', 'SB', 'D', 'ON']
        for i, lbl in enumerate(short):
            y = self.GRID_START_Y + i * row_h + row_h // 2 - 8
            draw.text((self.GRID_START_X - 55, y), lbl,
                      fill=self.COLOR_ACCENT, font=self.font_orb)

        
        draw.rectangle(
            [self.GRID_START_X, self.GRID_START_Y,
             self.GRID_START_X + self.GRID_WIDTH,
             self.GRID_START_Y + self.GRID_HEIGHT],
            outline=self.COLOR_ACCENT, width=1
        )

    
    def _draw_status_graph(self, draw: ImageDraw.Draw,
                           schedule_segments: List[Dict]):
        px_per_hr = self.GRID_WIDTH / self.HOURS_IN_DAY
        row_h     = self.GRID_HEIGHT // 4

        for seg in schedule_segments:
            start    = seg.get('start_time', 0)
            end      = seg.get('end_time',   0)
            activity = seg.get('activity',   '')
            status   = seg.get('status',    'off_duty')

            
            if status == 'driving':
                st = 'driving'
            elif activity in ['pickup', 'dropoff', 'fuel_stop']:
                st = 'on_duty'
            elif activity == 'required_rest':
                st = 'sleeper'
            else:
                st = 'off_duty'

            info = self.STATUS_MAP[st]
            x0   = self.GRID_START_X + int(start * px_per_hr)
            x1   = self.GRID_START_X + int(end   * px_per_hr)
            y0   = self.GRID_START_Y + info['y_position'] * row_h
            pad  = 4

            if x1 - x0 < 2:
                continue

            self._draw_rect_glow(draw,
                                 x0, y0 + pad,
                                 x1, y0 + row_h - pad,
                                 info['color'], info['glow'])

    
    def _draw_summary(self, draw: ImageDraw.Draw,
                      schedule_segments: List[Dict]):
        sy = self.GRID_START_Y + self.GRID_HEIGHT + 52

        
        total_driving = total_on_duty = total_off_duty = 0
        for seg in schedule_segments:
            dur      = seg.get('duration', 0)
            activity = seg.get('activity', '')
            status   = seg.get('status',   '')

            if status == 'driving':
                total_driving  += dur
                total_on_duty  += dur
            elif activity in ['pickup', 'dropoff', 'fuel_stop', 'required_break']:
                total_on_duty  += dur
            elif activity == 'required_rest':
                total_off_duty += dur

        items = [
            ('DRIVING',   f"{total_driving:.1f} HRS",  self.GLOW_DRIVING),
            ('ON DUTY',   f"{total_on_duty:.1f} HRS",  self.GLOW_ONDUTY),
            ('OFF DUTY',  f"{total_off_duty:.1f} HRS", self.GLOW_OFFDUTY),
        ]

        box_w = 220
        gap   = 24
        x     = self.GRID_START_X

        for label, value, glow in items:
            
            draw.rectangle([x, sy, x + box_w, sy + 68],
                           fill='#040e18')
            draw.rectangle([x, sy, x + box_w, sy + 68],
                           outline='#0a3d52', width=1)
            
            draw.rectangle([x, sy, x + 3, sy + 68], fill=glow)
            
            draw.rectangle([x, sy, x + box_w, sy + 1], fill=glow)

            draw.text((x + 12, sy + 10), label,
                      fill=self.COLOR_MUTED, font=self.font_orb)
            draw.text((x + 12, sy + 30), value,
                      fill=self.COLOR_ACCENT, font=self.font_title)
            x += box_w + gap

        
        draw.text(
            (self.GRID_START_X + 3 * (box_w + gap) + 20, sy + 22),
            "FMCSA 70-HR / 8-DAY RULE",
            fill=self.COLOR_MUTED, font=self.font_tiny
        )
        draw.text(
            (self.GRID_START_X + 3 * (box_w + gap) + 20, sy + 38),
            "§ 395.3  |  HOS COMPLIANT",
            fill='#005566', font=self.font_tiny
        )

    
    def generate_multiple_logs(
        self,
        all_schedule_segments: List[Dict],
        driver_name: str = "Driver",
    ) -> List[str]:
        days: Dict[int, list] = {}
        for seg in all_schedule_segments:
            d = seg.get('day', 0)
            days.setdefault(d, []).append(seg)

        logs = []
        for day_num in sorted(days.keys()):
            date = (datetime.now() + timedelta(days=day_num)).strftime('%Y-%m-%d')
            logs.append(self.generate_daily_log(
                day_num + 1, days[day_num], driver_name, date
            ))
        return logs
