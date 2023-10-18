function RGBtoHSV() {
    let r = document.getElementById("rgb-r").value / 255;
    let g = document.getElementById("rgb-g").value / 255;
    let b = document.getElementById("rgb-b").value / 255;
    let cmax = Math.max(r, g, b)
    let cmin = Math.min(r, g, b)
    let delta = cmax - cmin

    let h
    if (delta == 0) {
        h = 0
    } else if (cmax === r) {
        h = 60 * ((g - b) / delta)
    } else if (cmax === g) {
        h = 60 * ((b - r) / delta + 2)
    } else {
        h = 60 * ((r - g) / delta + 4)
    }
    if (h < 0) {
        h += 360;
    }
    h %= 360;

    let s
    if (cmax === 0) {
        s = 0
    } else {
        s = delta / cmax
    }
    let v = cmax

    document.getElementById("hsv-h").value = h
    document.getElementById("hsv-s").value = s * 100
    document.getElementById("hsv-v").value = v * 100

    document.getElementById("hsv-h-range").value = document.getElementById("hsv-h").value
    document.getElementById("hsv-s-range").value = document.getElementById("hsv-s").value
    document.getElementById("hsv-v-range").value = document.getElementById("hsv-v").value
}

function RGBtoCMYK() {
    let r = document.getElementById("rgb-r").value;
    let g = document.getElementById("rgb-g").value;
    let b = document.getElementById("rgb-b").value;
    if (r == 0 && g == 0 && b == 0) {
        document.getElementById("cmyk-k").value = 1;
        document.getElementById("cmyk-k-range").value = 1;

        document.getElementById("cmyk-c").value = 0;
        document.getElementById("cmyk-m").value = 0;
        document.getElementById("cmyk-y").value = 0;
    } else {
        document.getElementById("cmyk-k").value = 0;
        document.getElementById("cmyk-c").value = 1 - r / 255;
        document.getElementById("cmyk-m").value = 1 - g / 255;
        document.getElementById("cmyk-y").value = 1 - b / 255;

        document.getElementById("cmyk-k-range").value = document.getElementById("cmyk-k").value
    }
    document.getElementById("cmyk-c-range").value = document.getElementById("cmyk-c").value * 100
    document.getElementById("cmyk-m-range").value = document.getElementById("cmyk-m").value * 100
    document.getElementById("cmyk-y-range").value = document.getElementById("cmyk-y").value * 100
}

function CMYKtoRGB() {
    let k = document.getElementById("cmyk-k").value;
    let c = document.getElementById("cmyk-c").value;
    let m = document.getElementById("cmyk-m").value;
    let y = document.getElementById("cmyk-y").value;
    if (k == 1) {
        document.getElementById("rgb-r").value = 0;
        document.getElementById("rgb-g").value = 0;
        document.getElementById("rgb-b").value = 0;
    } else {
        document.getElementById("rgb-r").value = (1 - c) * 255;
        document.getElementById("rgb-g").value = (1 - m) * 255;
        document.getElementById("rgb-b").value = (1 - y) * 255;
    }

    document.getElementById("rgb-r-range").value = document.getElementById("rgb-r").value
    document.getElementById("rgb-g-range").value = document.getElementById("rgb-g").value
    document.getElementById("rgb-b-range").value = document.getElementById("rgb-b").value
}

function HSVtoRGB() {
    let h = document.getElementById("hsv-h").value;
    let s = document.getElementById("hsv-s").value / 100;
    let v = document.getElementById("hsv-v").value / 100;
    if (s == 0) {
        document.getElementById("rgb-r").value = v * 255;
        document.getElementById("rgb-g").value = v * 255;
        document.getElementById("rgb-b").value = v * 255;
    } else {
        h %= 360;
        h /= 60
        let i = Math.floor(h)
        let m = v * (1 - s)
        let n = v * (1 - (h - i) * s)
        let k = v * (1 - (1 - (h - i)) * s)

        let r =  0
        let g = 0
        let b = 0
        switch (i) {
            case 0: {
                [r, g, b] = [v, k, m]
                break
            }
            case 1: {
                [r, g, b] = [n, v, m]
                break
            }
            case 2: {
                [r, g, b] = [m, v, k]
                break
            }
            case 3: {
                [r, g, b] = [m, n, v]
                break
            }
            case 4: {
                [r, g, b] = [k, m, v]
                break
            }
            case 5: {
                [r, g, b] = [v, m, n]
            }
        }

        document.getElementById("rgb-r").value = r * 255
        document.getElementById("rgb-g").value = g * 255
        document.getElementById("rgb-b").value = b * 255
    }

    document.getElementById("rgb-r-range").value = document.getElementById("rgb-r").value
    document.getElementById("rgb-g-range").value = document.getElementById("rgb-g").value
    document.getElementById("rgb-b-range").value = document.getElementById("rgb-b").value
}

function Draw() {
    let r = document.getElementById("rgb-r").value
    let g = document.getElementById("rgb-g").value
    let b = document.getElementById("rgb-b").value
    document.getElementById("color-preview").style.backgroundColor = `rgb(${r}, ${g}, ${b})`
}

function Recompute() {
    if (changed_type === "rgb") {
        RGBtoCMYK()
        RGBtoHSV()
    } else if (changed_type === "cmyk") {
        CMYKtoRGB()
        RGBtoHSV()
    } else if (changed_type === "hsv") {
        HSVtoRGB()
        RGBtoCMYK()
    }
    Draw()
    changed_type = "none"
}

let changed_type = "none"
let old_cmyk_values = new Map()
let old_rgb_values = new Map()
let old_hsv_values = new Map()

let cmyk_array = ["c", "m", "y", "k"]
for (let i = 0; i < 4; ++i) {
    let letter = cmyk_array[i]
    old_cmyk_values.set(letter, document.getElementById("cmyk-" + letter).value)

    document.getElementById("cmyk-" + letter).onfocus = function () {
        old_cmyk_values.set(letter, document.getElementById("cmyk-" + letter).value)
    }

    document.getElementById("cmyk-" + letter).addEventListener("change", function (event) {
        event.preventDefault();
        if (document.getElementById("cmyk-" + letter).value === "") {
            document.getElementById("cmyk-" + letter).value = old_cmyk_values.get(letter)
        } else {
            let new_value = document.getElementById("cmyk-" + letter).value
            if (new_value < 0 || new_value > 1 || (letter === "k" && new_value != 0 && new_value != 1)) {
                alert("Invalid value")
                document.getElementById("cmyk-" + letter).value = old_cmyk_values.get(letter)
            } else {
                let c = document.getElementById("cmyk-c").value
                let m = document.getElementById("cmyk-m").value
                let y = document.getElementById("cmyk-y").value
                let k = document.getElementById("cmyk-k").value
                if (k == 1 && (c != 0 || m != 0 || y != 0)) {
                    alert("Invalid values combination")
                    document.getElementById("cmyk-" + letter).value = old_cmyk_values.get(letter)
                } else {
                    changed_type = "cmyk"
                    if (letter !== "k") {
                        new_value *= 100
                    }
                    document.getElementById("cmyk-" + letter + "-range").value = new_value
                    Recompute()
                }
            }
        }
    });
}

for (let i = 0; i < 4; ++i) {
    let letter = cmyk_array[i]
    document.getElementById("cmyk-" + letter + "-range").addEventListener("change", function (event) {
        let c = document.getElementById("cmyk-c-range").value / 100
        let m = document.getElementById("cmyk-m-range").value / 100
        let y = document.getElementById("cmyk-y-range").value / 100
        let k = document.getElementById("cmyk-k-range").value
        if (k == 1 && (c != 0 || m != 0 || y != 0)) {
            alert("Invalid values combination")
            let old_range_value = old_cmyk_values.get(letter)
            if (letter !== "k") {
                old_range_value *= 100
            }
            document.getElementById("cmyk-" + letter + "-range").value = old_range_value
        } else {
            document.getElementById("cmyk-" + letter).value =
                document.getElementById("cmyk-" + letter + "-range").value / 100
            if (letter === "k") {
                document.getElementById("cmyk-" + letter).value *= 100
            }
            changed_type = "cmyk"
            Recompute()
        }
    })
}

let rgb_array = ["r", "g", "b"]
for (let i = 0; i < 3; ++i) {
    let letter = rgb_array[i]
    old_rgb_values.set(letter, document.getElementById("rgb-" + letter).value)

    document.getElementById("rgb-" + letter).onfocus = function () {
        old_rgb_values.set(letter, document.getElementById("rgb-" + letter).value)
    }

    document.getElementById("rgb-" + letter).addEventListener("change", function (event) {
        event.preventDefault();
        let new_value = document.getElementById("rgb-" + letter).value
        if (new_value === "") {
            document.getElementById("rgb-" + letter).value = old_rgb_values.get(letter)
        } else {
            if (new_value < 0 || new_value > 255) {
                alert("Invalid value")
                document.getElementById("rgb-" + letter).value = old_rgb_values.get(letter)
            } else {
                changed_type = "rgb"
                document.getElementById("rgb-" + letter + "-range").value = new_value
                Recompute()
            }
        }
    });
}

for (let i = 0; i < 3; ++i) {
    let letter = rgb_array[i]
    document.getElementById("rgb-" + letter + "-range").addEventListener("change", function (event) {
        document.getElementById("rgb-" + letter).value =
            document.getElementById("rgb-" + letter + "-range").value
        changed_type = "rgb"
        Recompute()
    })
}

let hsv_array = ["h", "s", "v"]
for (let i = 0; i < 3; ++i) {
    let letter = hsv_array[i]
    old_hsv_values.set(letter, document.getElementById("hsv-" + letter).value)

    document.getElementById("hsv-" + letter).onfocus = function () {
        old_hsv_values.set(letter, document.getElementById("hsv-" + letter).value)
    }

    document.getElementById("hsv-" + letter).addEventListener("change", function (event) {
        event.preventDefault();
        let new_value = document.getElementById("hsv-" + letter).value
        if (new_value === "") {
            document.getElementById("hsv-" + letter).value = old_hsv_values.get(letter)
        } else {
            if (letter === "h" && (new_value < 0 || new_value > 360) ||
                letter !== "h" && (new_value < 0 || new_value > 100)) {
                alert("Invalid value")
                document.getElementById("hsv-" + letter).value = old_hsv_values.get(letter)
            } else {
                document.getElementById("hsv-" + letter + "-range").value = new_value
                changed_type = "hsv"
                Recompute()
            }
        }
    });
}

for (let i = 0; i < 3; ++i) {
    let letter = hsv_array[i]
    document.getElementById("hsv-" + letter + "-range").addEventListener("change", function (event) {
        document.getElementById("hsv-" + letter).value =
            document.getElementById("hsv-" + letter + "-range").value
        changed_type = "hsv"
        Recompute()
    })
}

document.getElementById("canvas").getContext("2d").drawImage(document.getElementById("color-wheel"), 0, 0, 400, 400)

document.getElementById("canvas").onclick = function (event) {
    let x = event.pageX - document.getElementById("canvas").offsetLeft
    let y = event.pageY - document.getElementById("canvas").offsetTop
    let color = document.getElementById("canvas").getContext("2d").getImageData(x, y, 1, 1).data

    if (!(color[0] === 255 && color[1] === 255 && color[2] === 255)) {
        document.getElementById("rgb-r").value = color[0]
        document.getElementById("rgb-g").value = color[1]
        document.getElementById("rgb-b").value = color[2]

        document.getElementById("rgb-r-range").value = color[0]
        document.getElementById("rgb-g-range").value = color[1]
        document.getElementById("rgb-b-range").value = color[2]
        changed_type = "rgb"
        Recompute()
    }
}
