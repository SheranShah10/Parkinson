class SVGWriter:
    @staticmethod
    def draw_bar_chart(data, filepath):
        svg_start = '<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">\n'
        svg_end = '</svg>'
        
        bars = ""
        max_val = max(data.values())
        y_scale = 300 / max_val if max_val > 0 else 1
        
        x_offset = 50
        for label, val in data.items():
            h = val * y_scale
            bars += f'<rect x="{x_offset}" y="{350-h}" width="50" height="{h}" fill="#3498db" />\n'
            bars += f'<text x="{x_offset+5}" y="370" font-family="Arial" font-size="12">{label}</text>\n'
            x_offset += 100
            
        with open(filepath, "w") as f:
            f.write(svg_start + bars + svg_end)
