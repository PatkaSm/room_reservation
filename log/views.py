from datetime import datetime

from rest_framework import status
from rest_framework.response import Response

from log.models import Log
from easy_pdf.views import PDFTemplateView


class LogsPDFView(PDFTemplateView):
    template_name = 'invoice.html'
    pdf_filename = "Raport.pdf"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise ConnectionAbortedError('Nie jesteś zautoryzowany')
        if not request.user.is_admin:
            raise ConnectionAbortedError('Nie jesteś zautoryzowany')

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.strptime(self.request.GET.get('date', '1111-11-11'), '%Y-%m-%d').date()
        self.pdf_filename = "Raport{}.pdf".format(date)
        logs = Log.objects.filter(date=date)
        context['date'] = date
        context['logs'] = logs
        return context
