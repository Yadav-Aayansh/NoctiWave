// Logout 
document.getElementById('logoutLink').addEventListener('click', function (event) {
  event.preventDefault();
  $('#logoutModal').modal('show');
});

document.getElementById('confirmLogout').addEventListener('click', function () {
  window.location.href = '/logout';
});

// Delete camapign
document.querySelectorAll('.deleteCampaignLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var campaignId = button.getAttribute('data-campaign-id');
        var modal = document.getElementById('deleteCampaignModal-' + campaignId);
        $(modal).modal('show');
    });
});


// Accept ad request
document.querySelectorAll('.acceptAdRequestLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var adRequestId = button.getAttribute('data-ad-request-id');
        var modal = document.getElementById('acceptAdRequestModal-' + adRequestId);
        $(modal).modal('show');
    });
});

// Reject ad request
document.querySelectorAll('.rejectAdRequestLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var adRequestId = button.getAttribute('data-ad-request-id');
        var modal = document.getElementById('rejectAdRequestModal-' + adRequestId);
        $(modal).modal('show');
    });
});

// Delete ad request
document.querySelectorAll('.deleteAdRequestLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var adRequestId = button.getAttribute('data-ad-request-id');
        var modal = document.getElementById('deleteAdRequestModal-' + adRequestId);
        $(modal).modal('show');
    });
});

// Delete negotiation
document.querySelectorAll('.deleteNegotiationLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var negotiationId = button.getAttribute('data-negotiation-id');
        var modal = document.getElementById('deleteNegotiationModal-' + negotiationId);
        $(modal).modal('show');
    });
});


// Delete platform
document.querySelectorAll('.deletePlatformButton').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var platformId = button.getAttribute('data-platform-id');
        var modal = document.getElementById('deletePlatformModal-' + platformId);
        $(modal).modal('show');
    });
});

// Show Flag Influencer Modal
document.querySelectorAll('.flagInfluencerLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var influencerId = button.getAttribute('data-influencer-id');
        var modal = document.getElementById('flagInfluencerModal-' + influencerId);
        $(modal).modal('show');
    });
});

// Show Unflag Influencer Modal
document.querySelectorAll('.unflagInfluencerLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var influencerId = button.getAttribute('data-influencer-id');
        var modal = document.getElementById('unflagInfluencerModal-' + influencerId);
        $(modal).modal('show');
    });
});

// Show Delete Influencer Modal
document.querySelectorAll('.deleteInfluencerLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var influencerId = button.getAttribute('data-influencer-id');
        var modal = document.getElementById('deleteInfluencerModal-' + influencerId);
        $(modal).modal('show');
    });
});

// Show Flag Campaign Modal
document.querySelectorAll('.flagCampaignLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var campaignId = button.getAttribute('data-campaign-id');
        var modal = document.getElementById('flagCampaignModal-' + campaignId);
        $(modal).modal('show');
    });
});

// Show Unflag Campaign Modal
document.querySelectorAll('.unflagCampaignLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var campaignId = button.getAttribute('data-campaign-id');
        var modal = document.getElementById('unflagCampaignModal-' + campaignId);
        $(modal).modal('show');
    });
});

// Show Delete Campaign Modal
document.querySelectorAll('.deleteCampaignLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var campaignId = button.getAttribute('data-campaign-id');
        var modal = document.getElementById('deleteCampaignModal-' + campaignId);
        $(modal).modal('show');
    });
});

// Show Flag Sponsor Modal
document.querySelectorAll('.flagSponsorLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var sponsorId = button.getAttribute('data-sponsor-id');
        var modal = document.getElementById('flagSponsorModal-' + sponsorId);
        $(modal).modal('show');
    });
});

// Show Unflag Sponsor Modal
document.querySelectorAll('.unflagSponsorLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var sponsorId = button.getAttribute('data-sponsor-id');
        var modal = document.getElementById('unflagSponsorModal-' + sponsorId);
        $(modal).modal('show');
    });
});

// Show Delete Sponsor Modal
document.querySelectorAll('.deleteSponsorLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var sponsorId = button.getAttribute('data-sponsor-id');
        var modal = document.getElementById('deleteSponsorModal-' + sponsorId);
        $(modal).modal('show');
    });
});


// Show View Ad Request Modal
document.querySelectorAll('[data-bs-toggle="modal"]').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var targetModal = button.getAttribute('data-bs-target');
        $(targetModal).modal('show');
    });
});

// Show View Ad Request Modal Copy
document.querySelectorAll('[data-bs-toggle="modal-copy"]').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var targetModal = button.getAttribute('data-bs-target');
        $(targetModal).modal('show');
    });
});

// Show Flag Ad Request Modal
document.querySelectorAll('.flagAdRequestLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var adRequestId = button.getAttribute('data-ad-request-id');
        var modal = document.getElementById('flagAdRequestModal-' + adRequestId);
        $(modal).modal('show');
    });
});

// Show Unflag Ad Request Modal
document.querySelectorAll('.unflagAdRequestLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var adRequestId = button.getAttribute('data-ad-request-id');
        var modal = document.getElementById('unflagAdRequestModal-' + adRequestId);
        $(modal).modal('show');
    });
});

// Show Delete Ad Request Modal
document.querySelectorAll('.deleteAdRequestLink').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var adRequestId = button.getAttribute('data-ad-request-id');
        var modal = document.getElementById('deleteAdRequestModal-' + adRequestId);
        $(modal).modal('show');
    });
});

// Show Delete Ad Request Modal Copy
document.querySelectorAll('.deleteAdRequestLinkCopy').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var adRequestId = button.getAttribute('data-ad-request-id');
        var modal = document.getElementById('deleteAdRequestModalCopy-' + adRequestId);
        $(modal).modal('show');
    });
});


// Search Influencer
$(document).ready(function () {
    var delayTimer;
    var selectedInfluencerIdInput = $('#selectedInfluencerId');

    $('#influencerUsername').on('input', function () {
        clearTimeout(delayTimer);
        var query = $(this).val();
        if (query.length > 2) {
            delayTimer = setTimeout(function () {
                $.ajax({
                    url: `/api/search_influencer/${encodeURIComponent(query)}`,
                    type: 'GET',
                    success: function (data) {
                        var resultsContainer = $('#influencerResults');
                        resultsContainer.empty();
                        if (Array.isArray(data) && data.length) {
                            data.forEach(function (influencer) {
                                resultsContainer.append(
                                    `<a href="#" class="list-group-item list-group-item-action" data-id="${influencer.influencer_id}">
                                        <strong>${influencer.name}</strong> (@${influencer.username})<br>
                                    </a>`
                                );
                            });

                            // Add click event to each result
                            resultsContainer.find('.list-group-item').on('click', function (e) {
                                e.preventDefault();
                                var influencer_id = $(this).data('id');
                                selectedInfluencerIdInput.val(influencer_id); 
                                $('#influencerUsername').val($(this).find('strong').text());
                                resultsContainer.empty();
                                resultsContainer.css('overflow-y', 'hidden'); 
                            });

                            if (resultsContainer.prop('scrollHeight') > resultsContainer.innerHeight()) {
                                resultsContainer.css('overflow-y', 'auto');
                            } else {
                                resultsContainer.css('overflow-y', 'hidden');
                            }
                        } else {
                            resultsContainer.append('<div class="list-group-item">No influencers found</div>');
                            resultsContainer.css('overflow-y', 'hidden');
                        }
                    },
                    error: function (xhr, status, error) {
                        console.error('Error fetching influencers:', error);
                        var resultsContainer = $('#influencerResults');
                        resultsContainer.empty().append('<div class="list-group-item">Error fetching influencers. Please try again later.</div>');
                    }
                });
            }, 300); // Delay in milliseconds
        } else {
            $('#influencerResults').empty();
            $('#influencerResults').css('overflow-y', 'hidden');
        }
    });

    // Search button click event (optional)
    $('#searchButton').on('click', function () {
        var query = $('#influencerUsername').val();
        var resultsContainer = $('#influencerResults');
        resultsContainer.empty();
        if (query.length > 2) {
            $.ajax({
                url: `/api/search_influencer/${encodeURIComponent(query)}`,
                type: 'GET',
                success: function (data) {
                    if (Array.isArray(data) && data.length) {
                        data.forEach(function (influencer) {
                            resultsContainer.append(
                                `<a href="#" class="list-group-item list-group-item-action" data-id="${influencer.influencer_id}">
                                    <strong>${influencer.name}</strong> (@${influencer.username})<br>
                                </a>`
                            );
                        });

                        // Add click event to each result
                        resultsContainer.find('.list-group-item').on('click', function (e) {
                            e.preventDefault();
                            var influencer_id = $(this).data('id');
                            selectedInfluencerIdInput.val(influencer_id); 
                            $('#influencerUsername').val($(this).find('strong').text());
                            resultsContainer.empty();
                            resultsContainer.css('overflow-y', 'hidden'); 
                        });

                        // Adjust container height and overflow
                        if (resultsContainer.prop('scrollHeight') > resultsContainer.innerHeight()) {
                            resultsContainer.css('overflow-y', 'auto');
                        } else {
                            resultsContainer.css('overflow-y', 'hidden');
                        }
                    } else {
                        resultsContainer.append('<div class="list-group-item">No influencers found</div>');
                        resultsContainer.css('overflow-y', 'hidden');
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Error fetching influencers:', error);
                    resultsContainer.empty().append('<div class="list-group-item">Error fetching influencers. Please try again later.</div>');
                }
            });
        } else {
            $('#influencerResults').css('overflow-y', 'hidden');
        }
    });
});

$(document).ready(function () {
    var delayTimers = {};

    $('[id^=influencerUsername-]').each(function () {
        var campaignId = $(this).attr('id').split('-')[1];
        var influencerUsernameInput = $('#influencerUsername-' + campaignId);
        var selectedInfluencerIdInput = $('#selectedInfluencerId-' + campaignId);
        var searchButton = $('#searchButton-' + campaignId);
        var resultsContainer = $('#influencerResults-' + campaignId);

        influencerUsernameInput.on('input', function () {
            clearTimeout(delayTimers[campaignId]);
            var query = $(this).val();
            if (query.length > 2) {
                delayTimers[campaignId] = setTimeout(function () {
                    $.ajax({
                        url: `/api/search_influencer/${encodeURIComponent(query)}`,
                        type: 'GET',
                        success: function (data) {
                            resultsContainer.empty();
                            if (Array.isArray(data) && data.length) {
                                data.forEach(function (influencer) {
                                    resultsContainer.append(
                                        `<a href="#" class="list-group-item list-group-item-action" data-id="${influencer.influencer_id}">
                                            <strong>${influencer.name}</strong> (@${influencer.username})<br>
                                        </a>`
                                    );
                                });

                                // Add click event to each result
                                resultsContainer.find('.list-group-item').on('click', function (e) {
                                    e.preventDefault();
                                    var influencer_id = $(this).data('id');
                                    selectedInfluencerIdInput.val(influencer_id);
                                    influencerUsernameInput.val($(this).find('strong').text());
                                    resultsContainer.empty();
                                    resultsContainer.css('overflow-y', 'hidden'); 
                                });

                                if (resultsContainer.prop('scrollHeight') > resultsContainer.innerHeight()) {
                                    resultsContainer.css('overflow-y', 'auto');
                                } else {
                                    resultsContainer.css('overflow-y', 'hidden');
                                }
                            } else {
                                resultsContainer.append('<div class="list-group-item">No influencers found</div>');
                                resultsContainer.css('overflow-y', 'hidden');
                            }
                        },
                        error: function (xhr, status, error) {
                            console.error('Error fetching influencers:', error);
                            resultsContainer.empty().append('<div class="list-group-item">Error fetching influencers. Please try again later.</div>');
                        }
                    });
                }, 300);
            } else {
                resultsContainer.empty();
                resultsContainer.css('overflow-y', 'hidden');
            }
        });

        // Search button click event (optional)
        searchButton.on('click', function () {
            var query = influencerUsernameInput.val();
            resultsContainer.empty();
            if (query.length > 2) {
                $.ajax({
                    url: `/api/search_influencer/${encodeURIComponent(query)}`,
                    type: 'GET',
                    success: function (data) {
                        if (Array.isArray(data) && data.length) {
                            data.forEach(function (influencer) {
                                resultsContainer.append(
                                    `<a href="#" class="list-group-item list-group-item-action" data-id="${influencer.influencer_id}">
                                        <strong>${influencer.name}</strong> (@${influencer.username})<br>
                                    </a>`
                                );
                            });

                            // Add click event to each result
                            resultsContainer.find('.list-group-item').on('click', function (e) {
                                e.preventDefault();
                                var influencer_id = $(this).data('id');
                                selectedInfluencerIdInput.val(influencer_id); 
                                influencerUsernameInput.val($(this).find('strong').text());
                                resultsContainer.empty();
                                resultsContainer.css('overflow-y', 'hidden'); 
                            });

                            if (resultsContainer.prop('scrollHeight') > resultsContainer.innerHeight()) {
                                resultsContainer.css('overflow-y', 'auto');
                            } else {
                                resultsContainer.css('overflow-y', 'hidden');
                            }
                        } else {
                            resultsContainer.append('<div class="list-group-item">No influencers found</div>');
                            resultsContainer.css('overflow-y', 'hidden');
                        }
                    },
                    error: function (xhr, status, error) {
                        console.error('Error fetching influencers:', error);
                        resultsContainer.empty().append('<div class="list-group-item">Error fetching influencers. Please try again later.</div>');
                    }
                });
            } else {
                resultsContainer.css('overflow-y', 'hidden');
            }
        });
    });
});


$(document).ready(function () {
    var delayTimer;
    var selectedCampaignIdInput = $('#selectedCampaignId');

    $('#campaignName').on('input', function () {
        clearTimeout(delayTimer);
        var query = $(this).val();
        if (query.length > 2) {
            delayTimer = setTimeout(function () {
                $.ajax({
                    url: `/api/campaign/${encodeURIComponent(query)}`,
                    type: 'GET',
                    success: function (data) {
                        var resultsContainer = $('#campaignResults');
                        resultsContainer.empty();
                        if (Array.isArray(data) && data.length) {
                            data.forEach(function (campaign) {
                                resultsContainer.append(
                                    `<a href="#" class="list-group-item list-group-item-action" data-id="${campaign.campaign_id}" data-sponsor-id="${campaign.sponsor_id}">
                                        <strong>${campaign.name}</strong><br>
                                    </a>`
                                );
                            });

                            resultsContainer.find('.list-group-item').on('click', function (e) {
                                e.preventDefault();
                                var campaign_id = $(this).data('id');
                                var sponsor_id = $(this).data('sponsor-id');
                                selectedCampaignIdInput.val(campaign_id); 
                                $('#campaignName').val($(this).find('strong').text());
                                $('#sponsor_id').val(sponsor_id); 
                                resultsContainer.empty();
                                resultsContainer.css('overflow-y', 'hidden');
                            });

                            if (resultsContainer.prop('scrollHeight') > resultsContainer.innerHeight()) {
                                resultsContainer.css('overflow-y', 'auto');
                            } else {
                                resultsContainer.css('overflow-y', 'hidden');
                            }
                        } else {
                            resultsContainer.append('<div class="list-group-item">No campaigns found</div>');
                            resultsContainer.css('overflow-y', 'hidden');
                        }
                    },
                    error: function (xhr, status, error) {
                        console.error('Error fetching campaigns:', error);
                        var resultsContainer = $('#campaignResults');
                        resultsContainer.empty().append('<div class="list-group-item">Error fetching campaigns. Please try again later.</div>');
                    }
                });
            }, 300); 
        } else {
            $('#campaignResults').empty();
            $('#campaignResults').css('overflow-y', 'hidden');
        }
    });

    // Search button click event (optional)
    $('#searchCampaignButton').on('click', function () {
        var query = $('#campaignName').val();
        var resultsContainer = $('#campaignResults');
        resultsContainer.empty();
        if (query.length > 2) {
            $.ajax({
                url: `/api/campaign/${encodeURIComponent(query)}`,
                type: 'GET',
                success: function (data) {
                    if (Array.isArray(data) && data.length) {
                        data.forEach(function (campaign) {
                            resultsContainer.append(
                                `<a href="#" class="list-group-item list-group-item-action" data-id="${campaign.campaign_id}" data-sponsor-id="${campaign.sponsor_id}">
                                    <strong>${campaign.name}</strong><br>
                                </a>`
                            );
                        });

                       
                        resultsContainer.find('.list-group-item').on('click', function (e) {
                            e.preventDefault();
                            var campaign_id = $(this).data('id');
                            var sponsor_id = $(this).data('sponsor-id');
                            selectedCampaignIdInput.val(campaign_id); 
                            $('#campaignName').val($(this).find('strong').text());
                            $('#sponsor_id').val(sponsor_id);
                            resultsContainer.empty();
                            resultsContainer.css('overflow-y', 'hidden'); 
                        });

                    
                        if (resultsContainer.prop('scrollHeight') > resultsContainer.innerHeight()) {
                            resultsContainer.css('overflow-y', 'auto');
                        } else {
                            resultsContainer.css('overflow-y', 'hidden');
                        }
                    } else {
                        resultsContainer.append('<div class="list-group-item">No campaigns found</div>');
                        resultsContainer.css('overflow-y', 'hidden');
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Error fetching campaigns:', error);
                    resultsContainer.empty().append('<div class="list-group-item">Error fetching campaigns. Please try again later.</div>');
                }
            });
        } else {
            $('#campaignResults').css('overflow-y', 'hidden');
        }
    });
});

// Event listener for the Remove Picture button
document.getElementById('removePictureButton').addEventListener('click', function() {
    $('#removePictureModal').modal('show'); 
});