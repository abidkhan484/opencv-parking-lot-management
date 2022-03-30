$(document).ready(function () {
    const finalArrayOfCoordinates = [];
    var linesArray = [];

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

    canvas.addEventListener("mousedown", function(e)
    {
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

});
