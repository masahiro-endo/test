
import pyxel as px








class Meth:
    
    @staticmethod
    def draw_filled_polygon(points, col):
        # """
        # Draws a filled polygon using triangle fan method.
        # points: list of (x, y) tuples
        # col: Pyxel color index (0-15)
        # """
        if len(points) < 3:
            return  # Not a polygon

        x0, y0 = points[0]
        for i in range(1, len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            px.tri(x0, y0, x1, y1, x2, y2, col)

    # Helper: draw polygon outline
    @staticmethod
    def draw_polygon_outline(points, col):
        # """
        # Draws polygon outline by connecting points in order.
        # """
        if len(points) < 2:
            return
        
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]
            px.line(x1, y1, x2, y2, col)


