Highcharts.theme = {
    colors: [
        '#428bca',
        '#5cb85c',
        '#f0ad4e',
        '#d9534f',
        '#790CE8',
        '#5bc0de',
        '#38c79e'
    ],
    chart: {
        style: {
            fontFamily: '"Open Sans","Helvetica Neue",Helvetica,Arial,sans-serif',
        },
        height: 250
    },
    title: {
        style: {
            fontFamily: '"Open Sans","Helvetica Neue",Helvetica,Arial,sans-serif',
            color: '#666',
            fontWeight: 'bold'
        }
    },
    credits: {
        enabled: false
    },
    xAxis: {
        labels: {
            style: {
                fontFamily: '"Open Sans","Helvetica Neue",Helvetica,Arial,sans-serif',
                color: '#666'
            }
        }
    },
    yAxis: {
        title: {
            style: {
                fontFamily: '"Open Sans","Helvetica Neue",Helvetica,Arial,sans-serif',
                color: '#999'
            }
        },
        labels: {
            style: {
                fontFamily: '"Open Sans","Helvetica Neue",Helvetica,Arial,sans-serif',
                color: '#999'
            }
        }
    },
    tooltip: {
		borderRadius: 0,
    },
    plotOptions: {
		pie: {
			dataLabels: {
				formatter: function(){
					return this.key + ' (' + this.y + ')';
				}
			}
		}
    }

};
Highcharts.setOptions(Highcharts.theme);