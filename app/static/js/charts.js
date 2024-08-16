// Chart 1: Campaign Distribution by Category (Bar Chart)
var ctx1 = document.getElementById('campaignChart');
if (ctx1) {
    var myBarChart = new Chart(ctx1.getContext('2d'), {
        type: 'bar',
        data: chartData,
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Campaign Distribution by Category'
            },
            barPercentage: 0.7,
            categoryPercentage: 0.8
        }
    });
}


// Chart 2: Sponsor Influencer Ratio (Pie Chart)
var ctx2 = document.getElementById('sponsorInfluencerChart');
if (ctx2) {
    var myPieChart = new Chart(ctx2.getContext('2d'), {
        type: 'doughnut',
        data: chartData2,
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Sponsor Influencer Ratio'
            }
        }
    });
}

// Chart 3: Ad Request Status (Stacked Bar Chart)
var ctx3 = document.getElementById('adrequestStatus');
if (ctx3) {
    var myBarChart2 = new Chart(ctx3.getContext('2d'), {
        type: 'bar',
        data: chartData3,
        options: {
            responsive: true,
            scales: {
                xAxes: [{
                    stacked: true
                }],
                yAxes: [{
                    stacked: true
                }]
            },
            title: {
                display: true,
                text: 'Ad Request Status'
            }
        }
    });
}

// Chart 4: Flagged Non-Flagged Ratio (Pie Chart)
var ctx4 = document.getElementById('flaggedCampaign');
if (ctx4) {
    var myPieChart2 = new Chart(ctx4.getContext('2d'), {
        type: 'doughnut',
        data: chartData4,
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Flagged Non-Flagged Ratio'
            }
        }
    });
}

// Chart 5: Private Public Ratio (Pie Chart)
var ctx5 = document.getElementById('privateCampaign');
if (ctx5) {
    var myPieChart3 = new Chart(ctx5.getContext('2d'), {
        type: 'doughnut',
        data: chartData5,
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Private Public Ratio'
            }
        }
    });
}

// Chart 6: Influencer Distribution by Category (Bar Chart)
var ctx6 = document.getElementById('influencerChart');
if (ctx6) {
    var myBarChart2 = new Chart(ctx6.getContext('2d'), {
        type: 'bar',
        data: chartData6,
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Influencer Distribution by Category'
            },
            barPercentage: 0.7,
            categoryPercentage: 0.8
        }
    });
}

// Chart 7: Flagged Non-Flagged Ratio (Pie Chart)
var ctx7 = document.getElementById('flaggedInfluencer');
if (ctx7) {
    var myPieChart4 = new Chart(ctx7.getContext('2d'), {
        type: 'doughnut',
        data: chartData7,
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Flagged Non-Flagged Ratio'
            }
        }
    });
}

// Chart 8: Influencer Platfrom (Pie Chart)
var ctx8 = document.getElementById('influencerPlatform');
if (ctx8) {
    var myPieChart4 = new Chart(ctx8.getContext('2d'), {
        type: 'doughnut',
        data: chartData8,
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Influencer by Platfrom'
            }
        }
    });
}

// Chart 9: Sponsor Distribution by Category (Bar Chart)
var ctx9 = document.getElementById('sponsorChart');
if (ctx9) {
    var myBarChart3 = new Chart(ctx9.getContext('2d'), {
        type: 'bar',
        data: chartData9,
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Sponsor Distribution by Category'
            },
            barPercentage: 0.7,
            categoryPercentage: 0.8
        }
    });
}

// Chart 10: Flagged Non-Flagged Ratio (Pie Chart)
var ctx10 = document.getElementById('flaggedSponsor');
if (ctx10) {
    var myPieChart5 = new Chart(ctx10.getContext('2d'), {
        type: 'doughnut',
        data: chartData10,
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Flagged Non-Flagged Ratio'
            }
        }
    });
}

// Chart 11: Sponsor Distribution by budget (Bar Chart)
var ctx11 = document.getElementById('sponsorChartBudget');
if (ctx11) {
    var myBarChart4 = new Chart(ctx11.getContext('2d'), {
        type: 'doughnut',
        data: chartData11,
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Sponsor Distribution by Budget'
            },
            barPercentage: 0.7,
            categoryPercentage: 0.8
        }
    });
}

// Chart 12: AdRequest Distribution by Category (Bar Chart)
var ctx12 = document.getElementById('adRequestChart');
if (ctx12) {
    var myBarChart5 = new Chart(ctx12.getContext('2d'), {
        type: 'bar',
        data: chartData12,
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Ad Request Distribution by Category'
            },
            barPercentage: 0.7,
            categoryPercentage: 0.8
        }
    });
}

// Chart 13: Flagged Non-Flagged Ratio (Pie Chart)
var ctx13 = document.getElementById('flaggedAdRequest');
if (ctx13) {
    var myPieChart13 = new Chart(ctx13.getContext('2d'), {
        type: 'doughnut',
        data: chartData13,
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Flagged Non-Flagged Ratio'
            }
        }
    });
}

// Chart 14: Flagged Non-Flagged Ratio (Pie Chart)
var ctx14 = document.getElementById('adRequestStatus');
if (ctx14) {
    var myPieChart14 = new Chart(ctx14.getContext('2d'), {
        type: 'doughnut',
        data: chartData14,
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Flagged Non-Flagged Ratio'
            }
        }
    });
}

// Chart 15: Everything (Bar Chart)
var ctx15 = document.getElementById('everythingChart');
if (ctx15) {
    var myBarChart15 = new Chart(ctx15.getContext('2d'), {
        type: 'bar',
        data: {
            "labels": ["User", "Influencer", "Sponsor", "Campaign", "AdRequest", "Negotiation"],
            "datasets": [{
                "data": counts,
                "label": 'Overall Analysis',
                "backgroundColor": [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',
                    'rgba(255, 159, 64, 0.5)',
                    'rgba(0, 255, 0, 0.5)',   
                    'rgba(255, 215, 0, 0.5)',
                    'rgba(186, 85, 211, 0.5)', 
                    'rgba(255, 69, 0, 0.5)'  
                ]
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Overall Analysis'
            },
            barPercentage: 0.7,
            categoryPercentage: 0.8
        }
    });
}