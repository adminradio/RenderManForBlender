<script type="text/javascript" charset="utf-8">
    window.onload = function () {
        var r = Raphael("holder", 620, 420),
            discattr = {fill: "#fff", stroke: "none"};
        //r.rect(0, 0, 619, 419, 10).attr({stroke: "#666"});
        r.text(310, 40, "Drag the points to change the curves").attr({fill: "#fff", "font-size": 16});
        function curve(x, y, ax, ay, bx, by, zx, zy, color) {
            var path = [["M", x, y], ["C", ax, ay, bx, by, zx, zy]],
                path2 = [["M", x, y], ["L", ax, ay], ["M", bx, by], ["L", zx, zy]],
                curve = r.path(path).attr({stroke: color || Raphael.getColor(), "stroke-width": 4, "stroke-linecap": "round"}),
                controls = r.set(
                    r.path(path2).attr({stroke: "#ccc", "stroke-dasharray": ". "}),
                    r.circle(x, y, 5).attr(discattr),
                    r.circle(ax, ay, 5).attr(discattr),
                    r.circle(bx, by, 5).attr(discattr),
                    r.circle(zx, zy, 5).attr(discattr)
                );
            controls[1].update = function (x, y) {
                var X = this.attr("cx") + x,
                    Y = this.attr("cy") + y;
                this.attr({cx: X, cy: Y});
                path[0][1] = X;
                path[0][2] = Y;
                path2[0][1] = X;
                path2[0][2] = Y;
                controls[2].update(x, y);
            };
            controls[2].update = function (x, y) {
                var X = this.attr("cx") + x,
                    Y = this.attr("cy") + y;
                this.attr({cx: X, cy: Y});
                path[1][1] = X;
                path[1][2] = Y;
                path2[1][1] = X;
                path2[1][2] = Y;
                curve.attr({path: path});
                controls[0].attr({path: path2});
            };
            controls[3].update = function (x, y) {
                var X = this.attr("cx") + x,
                    Y = this.attr("cy") + y;
                this.attr({cx: X, cy: Y});
                path[1][3] = X;
                path[1][4] = Y;
                path2[2][1] = X;
                path2[2][2] = Y;
                curve.attr({path: path});
                controls[0].attr({path: path2});
            };
            controls[4].update = function (x, y) {
                var X = this.attr("cx") + x,
                    Y = this.attr("cy") + y;
                this.attr({cx: X, cy: Y});
                path[1][5] = X;
                path[1][6] = Y;
                path2[3][1] = X;
                path2[3][2] = Y;
                controls[3].update(x, y);
            };
            controls.drag(move, up);
        }
        function move(dx, dy) {
            this.update(dx - (this.dx || 0), dy - (this.dy || 0));
            this.dx = dx;
            this.dy = dy;
        }
        function up() {
            this.dx = this.dy = 0;
        }
        curve( 70, 100, 110, 100, 130, 300, 170, 300, "hsb( 0, .75, .75)");
        curve(170, 100, 210, 100, 230, 300, 270, 300, "hsb(.8, .75, .75)");
        curve(270, 100, 310, 100, 330, 300, 370, 300, "hsb(.3, .75, .75)");
        curve(370, 100, 410, 100, 430, 300, 470, 300, "hsb(.6, .75, .75)");
        curve(470, 100, 510, 100, 530, 300, 570, 300, "hsb(.1, .75, .75)");
    };
</script>
<div id="holder" style="background-color: #222; text-align: center;"></div>
