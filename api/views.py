from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .scraper import scrape_data, handle_zip_captcha
from .models import Tender
from .utils.storage import upload_to_gcs
from tender.settings.base import GCS_TENDER_ZIP_BUCKET

import requests
@api_view(["GET"])
def check(request: Request):
    return Response("I'm alive", status=200)

@api_view(["GET"])
def scrape(request: Request):
    status, data = scrape_data()
    if status:
        print(data)
        for tender in data:
            print("Checking if tender exists")
            check = Tender.objects.filter(ref_no=tender.get("Tender Reference Number"))
            print("Checked")
            if check:
                # If the tender already exists in the database, skip it (Might make it an "update")
                continue

            public_url = None

            print("Downloading zip")
            def get_zip(tender):
                #Need to handle captcha for file download (Probably need to use selenium, instead of requests)
                if tender.get("zip"):
                    zip_response = requests.get(tender.get("zip"))
                    print(zip_response.headers.get('Content-Type'))
                    if zip_response.headers.get('Content-Type') == "application/zip":
                        upload_to_gcs(zip_response.content, GCS_TENDER_ZIP_BUCKET , f"{tender.get('Tender Reference Number')}.zip")
                    else:
                        print("Not zip")
                        print(tender)
                        return handle_zip_captcha(tender.get("zip"), tender.get(tender.get("Tender ID")))

            public_url = get_zip(tender)        
            Tender.objects.create(
                org_chain=tender.get("Organisation Chain"),
                ref_no=tender.get("Tender Reference Number"),
                tender_id=tender.get("Tender ID"),
                zip_url=public_url
            )
        return Response({"message": "Scraping successful"}, status=200)
        
    return Response({"message": "Scraping failed"}, status=500)

@api_view(["GET"])
def get_tenders(request: Request):
    tenders = Tender.objects.all()
    return Response({"tenders": tenders}, status=200)