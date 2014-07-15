dataDictionary = {}
chartData = [{
    color: "#000000",
    data: [{ x: 1, y: 2 }, { x:2, y: 2 }]
}]


graph = null;

$(document).ready(function () {
    load();


});

var load = function () {

    // Start Graph
    graph = new Rickshaw.Graph({
        element: document.querySelector("#chart"),
        width: 700,
        height: 320,
        renderer: 'line',
        series: chartData

    });


    var x_axis = new Rickshaw.Graph.Axis.Time({ graph: graph });

    var y_axis = new Rickshaw.Graph.Axis.Y({
        graph: graph,
        orientation: 'left',
        tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
        element: document.getElementById('y_axis'),
    });

    graph.render();

    // Set up panel
    queryData =
        {
            "metric": "*"
        };
    $.ajax({
        url: "http://134.82.132.101:8888/lookup",
        dataType: "json",
        error: loadFailed,
        success: showMetric,
        crossDomain: true,
        data: JSON.stringify(queryData),
        type: 'POST'
    });

    // Load time picker
    loadTimePicker();

    // hook up events
    $("#btnView").click(function ()
    { onViewClicked(); });
};

var showMetric = function (data, status, jqXHRob) {
    var metrics = [];
    var dic = jQuery.parseJSON(data);
    var results = dic["results"]
    jQuery.each(results, function (i, item) {
        if (jQuery.inArray(item["metric"], metrics) == -1) {
            metrics.push(item["metric"]);
            generatePanel(item["metric"]);
        }
        addItem(item["metric"], item["tags"]);
    });
}

var loadFailed = function () {
    console.log("LOG FAILED");
}


var generatePanel = function (name) {
    var strname = name.replace(".", "-");
    var div = "                    <div class='panel panel-default'><div class='panel-heading'>\
                            <a class='panel-title' data-toggle='collapse' data-parent='#panel-409101' href='#panel-element-" + strname + "'>" + name + "</a>\
                        </div>\
                        <div id='panel-element-" + strname + "' class='panel-collapse collapse in'>\
                        </div>\
                    </div>"
    $("#metrics").prepend(div);
    $("#panel-element-" + strname).collapse('hide');
}

var addItem = function (metric, tags) {
    var name = "";
    jQuery.each(tags, function (i, val) {
        name += i + " : " + val + '<br />';
    });

    var id = Math.floor(Math.random() * 1000000);
    dataDictionary[id] = { "metric": metric, "tags": tags };

    if (name == "") { name = "Empty" };
    strMetric = metric.replace(".", "-");

    var div = "<div class='panel-body'>\
                                <div class='checkbox'>\
                                    <label>\
                                        <input type='checkbox' id = '" + id + "'>" + name + "\
                                    </label>\
                                </div>\
                            </div>";
    $("#panel-element-" + strMetric).prepend(div);
    //$("#" + id.toString()).click(function (elem) {
    //    console.log(elem)
    //    var i = $(elem.target).attr("id");
    //    addData(i);
    //})
}

var addData = function (id) {
    var queryData= 
        {
            "start": 1400000000,
            "end": 1500000000,
            "queries": [{
                "metric": dataDictionary[id]["metric"],
                "tags": dataDictionary[id]["tags"],
                "aggregator": "max"
            }]
        }
    $.ajax({
        url: "http://localhost:8888/rickshaw",
        dataType: "json",
        error: loadFailed,
        success: updateData,
        crossDomain: true,
        data: JSON.stringify(queryData),
        type: 'POST'
    })
}

var updateData = function (data, status, jqXHRob) {
    var palette = new Rickshaw.Color.Palette();
    while (chartData.length > 0) {
        chartData.pop();
    }
    jQuery.each(data, function (i, dps) {
        dps = data[0]
        randColor = palette.color(); //Math.floor(Math.random() * 16777215).toString(16);
        jQuery.each(dps, function (i, value) {
            chartData.push({
                data: value,
                color: randColor
            });
        });
    });
    
    graph.update();
}

var loadTimePicker = function () {
    $("#start-time").datetimepicker({
        language: 'en',
        pick12HourFormat: true
    });
    $("#end-time").datetimepicker({
        language: 'en',
        pick12HourFormat: true
    });
}

var onViewClicked = function () {
    var start = $('#start-time').data("DateTimePicker").getDate().utc().unix();
    var end = $('#end-time').data("DateTimePicker").getDate().utc().unix();

    var queryData =
        {
            "start": start,
            "end": end
        }

    var checkList = $(':checkbox:checked')

    var strDownsameple = "";
    var difference = end - start;

    if (checkList.length <= 0 || difference <= 0) {
        alert("NOPE!");
    }

    if (difference > 2592000) {
        strDownsameple = "1d-avg";
    }
    else if (difference > 864000 && difference < 2592000) { // 10 days
        strDownsameple = "12h-avg";
    }


    jQuery.each(checkList, function (i, value) {
        var id = value.id;
        if (!("queries" in queryData )){
            queryData["queries"] = []
        }

        console.log(queryData);
        queryData["queries"].push({
            "metric": dataDictionary[id]["metric"],
            "tags": dataDictionary[id]["tags"],
            "aggregator": "max"
        })
    });

    $.ajax({
        url: "http://localhost:8888/rickshaw",
        dataType: "json",
        error: loadFailed,
        success: updateData,
        crossDomain: true,
        data: JSON.stringify(queryData),
        type: 'POST'
    })

}