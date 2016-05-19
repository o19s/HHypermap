
function gen_harvest_request(resourcetype, source) {
    xml = '<Harvest service="CSW" version="2.0.2" xmlns="http://www.opengis.net/cat/csw/2.0.2">';
    xml+= '<Source>' + source + '</Source>';
    xml+= '<ResourceType>' + resourcetype + '</ResourceType>';
    xml+= '</Harvest>';

    return xml;
}

$('#publish-resource').click(function(event) {
    var resourcetype = $('#csw-resourcetype').val();
    var source = $('#resource-url').attr('href');
    var csw_url = $('#csw-url').val();

    var harvest_request = gen_harvest_request(resourcetype, source);

    $.ajax({
        type: 'post',
        crossDomain: true,
        url: csw_url,
        data: harvest_request,
        dataType: 'text',
        success: function(xml) {
            alert(xml);
        }
    });
});
