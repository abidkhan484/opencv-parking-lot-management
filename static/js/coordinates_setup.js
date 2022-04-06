$(document).ready(function () {
    var canvas = document.querySelector("canvas#coordinate_generator_canvas"),
    context = canvas.getContext('2d'),
    lineWidth = 1,
    finalArrayOfCoordinates = [],
    linesArray = [];

    const getMousePosition = (canvas, event) => {
        let rect = canvas.getBoundingClientRect();
        let x = event.clientX - rect.left;
        let y = event.clientY - rect.top;
        return [x, y];
    }

    const createLine = (x1, y1, x2, y2) => {
        context.moveTo(x1, y1);
        context.lineTo(x2, y2);
        context.lineWidth = lineWidth;
        context.strokeStyle = '#ff0000';
        context.stroke();
    }

    $(document).on("mousedown", "canvas#coordinate_generator_canvas", (e) => {
        let x, y, x1, y1, arrayLength;
        [x, y] = getMousePosition(canvas, e);

        linesArray.push([x, y]);
        arrayLength = linesArray.length;
        if (arrayLength == 4) {
            finalArrayOfCoordinates.push(linesArray);
            [x1, y1] = linesArray[arrayLength - 2];
            createLine(x, y, x1, y1);
            [x1, y1] = linesArray[0];
            createLine(x, y, x1, y1);
            linesArray = [];
        }
        else if (arrayLength > 1) {
            [x1, y1] = linesArray[arrayLength - 2];
            createLine(x, y, x1, y1);
        }
    });

    $(document).on("click", "#capture_img", () => {
        context.clearRect(0, 0, IMAGE_WIDTH, IMAGE_HEIGHT);

        var img = document.getElementById("img");
        context.drawImage(img, 0, 0, IMAGE_WIDTH, IMAGE_HEIGHT);
        context.beginPath();
        encodedImg = canvas.toDataURL("image/png");

        // console.log(finalArrayOfCoordinates);
        finalArrayOfCoordinates = [];
        linesArray = [];
        $("#submit_coordinates").show();
    });

    $(document).on("click", "#submit_coordinates", function() {
        console.log(finalArrayOfCoordinates);
    });

});
