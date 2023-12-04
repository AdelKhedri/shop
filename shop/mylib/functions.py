def get_ipaddress(request):
    req_headers = request.META
    x_froward_for_value = req_headers.get("HTTP_X_FORWARD_FOR")
    if x_froward_for_value:
        ipaddress = x_froward_for_value.split(',').strip()
    else:
        ipaddress = req_headers.get("REMOTE_ADDR")
    return ipaddress