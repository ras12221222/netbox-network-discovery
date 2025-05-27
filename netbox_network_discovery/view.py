from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
import csv
import io
from .discovery import run_discovery

@staff_member_required
def discovery_view(request):
    results = run_discovery(start_device="core-switch-1", max_depth=2)

    if not results:
        return HttpResponse("No results", status=204)

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

    response = HttpResponse(buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="network_discovery.csv"'
    return response
