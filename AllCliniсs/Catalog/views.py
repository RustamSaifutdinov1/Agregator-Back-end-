from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from parsel import Selector
from .models import *
from .serializers import *


class DoctorsViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class ClinicsViewSet(viewsets.ModelViewSet):
    queryset = Clinics.objects.all()
    serializer_class = ClinicsSerializer

    @action(methods=['get'], detail=True)
    def doctors(self, request, pk=None):
        doc = Doctor.objects.filter(DoctorClinic=pk)
        doctors_list = []
        for d in doc:
            article = {
                'name': d.DoctorName,
                'content': d.DoctorContent,
                'photo': 'http://127.0.0.1:8000/media/' + str(d.DoctorPhoto),
            }
            doctors_list.append(article)
        return Response(doctors_list)

    @action(methods=['get'], detail=True)
    def services(self, request, pk=None):
        ser = Services.objects.filter(ServiceClinic=pk)
        service_list = []
        for s in ser:
            article = {
                'name': s.ServiceName,
                'price': s.ServicePrice,
                'photo': 'http://127.0.0.1:8000/media/' + str(s.ServicePhoto)
            }
            service_list.append(article)
        return Response(service_list)


class ClinicCategoryViewSet(viewsets.ModelViewSet):
    queryset = CategoryClinics.objects.all()
    serializer_class = CategoryClinicsSerializer

    @action(methods=['get'], detail=True)
    def clinics(self, request, pk=None):
        clinic = Clinics.objects.filter(ClinicCat=pk)
        clinic_list = []
        for c in clinic:
            article = {
                'name': c.ClinicName,
                'content': c.ClinicContent,
                'address': c.ClinicAddress,
                'telephone': c.ClinicTelephone,
                'work-time': c.ClinicWork_time,
                'pk': c.id,
            }
            clinic_list.append(article)
        return Response(clinic_list)


def ortus_rss():
    article_list_doc = []
    article_list_ser = []
    article_list_clinic = []
    try:
        r = requests.get('https://ortusdental.ru/')
        soup = BeautifulSoup(r.content, features='xml')
        content = soup.find('p', class_='elementor-image-box-description').text
        address = soup.find('span', class_='headeraddress').text
        telephone = soup.find('a', class_='wabuttonphone').text
        article = {
            'name': 'Ortus',
            'content': 'Обратившись в клинику «Ortus», Вы можете быть уверены, что получите качественное и '
                       'высокопрофессиональное лечение по доступным ценам',
            'address': address,
            'telephone': telephone,
            'work-time': content,
        }
        article_list_clinic.append(article)
        services = soup.findAll('div', class_="dopuslugi")
        for s in services:
            service_price = s.find('span', class_="dopprice").text
            service_name = s.find('span').text.replace(service_price, '')
            article = {
                'name': service_name,
                'price': service_price
            }
            article_list_ser.append(article)
        r = requests.get('https://ortusdental.ru/врачи/')
        soup = BeautifulSoup(r.content, features='xml')
        doctors_name = soup.findAll('h4', class_='elementor-heading-title elementor-size-default')
        doctors_attr1 = []
        doctors_attr2 = []
        for d in doctors_name:
            doctors = d.find('a')
            doctor_name = doctors.text
            doctors_attr1.append(doctor_name)
        doctors_content = soup.findAll('h5', class_='elementor-heading-title elementor-size-default')
        for d in doctors_content:
            doctors = d.find('a')
            doctor_content = doctors.text
            doctors_attr2.append(doctor_content)
        for i in range(len(doctors_attr1)):
            article = {
                'name': doctors_attr1[i],
                'content': doctors_attr2[i]
            }
            article_list_doc.append(article)
        return save_function(article_list_ser, article_list_doc, article_list_clinic)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)


def omicron_rss():
    article_list_doc = []
    article_list_ser = []
    article_list_clinic = []
    try:
        driver = webdriver.Edge()
        driver.get('https://omiclinic.ru/contacts/')
        address = driver.find_element(By.CLASS_NAME, 'contactCity__item-block').text
        telephone = driver.find_elements(By.CLASS_NAME, 'contactCity__item-block')[1].text
        work_time = driver.find_elements(By.CLASS_NAME, 'contactCity__item-block')[2].text
        driver.get('https://omiclinic.ru/about/')
        content = driver.find_element(By.CLASS_NAME, 'aboutTextBlock-text').text
        article = {
            'name': 'Омикрон',
            'address': address,
            'telephone': telephone,
            'work-time': work_time,
            'content': content
        }
        article_list_clinic.append(article)
        driver.get('https://omiclinic.ru/services/')
        services = driver.find_elements(By.CLASS_NAME, 'contactDocs__item-title')
        service = []
        for s in services:
            service.append(s.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        for i in service:
            driver.get(i)
            service_name = driver.find_element(By.CLASS_NAME, 'footer-nav').find_element(By.CLASS_NAME,
                                                                                         'item-selected').text
            service_price = driver.find_element(By.CLASS_NAME, 'promoServices-bottom').find_element(By.TAG_NAME,
                                                                                                    'span').text
            article = {
                'name': service_name,
                'price': service_price
            }
            article_list_ser.append(article)
        driver.get('https://omiclinic.ru/doctors/')
        doctors = driver.find_elements(By.CLASS_NAME, 'doctors__item-block')
        for d in doctors:
            try:
                d.find_element(By.CLASS_NAME, 'doctors__item-toggle').click()
            except Exception as e:
                continue
            doc_name = d.find_element(By.CLASS_NAME, 'doctors__item-title').text
            doc_content = d.find_element(By.CLASS_NAME, 'doctors__item-text').text
            article = {
                'name': doc_name,
                'content': doc_content
            }
            article_list_doc.append(article)
        return save_function(article_list_ser, article_list_doc, article_list_clinic)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)


def neo_rss():
    article_list_doc = []
    article_list_ser = []
    article_list_clinic = []
    try:
        r = requests.get('https://mc-neo.ru/')
        soup = BeautifulSoup(r.content, features='xml')
        content = soup.find('p', class_='about__text').text
        address = soup.find('a', class_='header__address').text
        telephone = soup.find('a', class_='header__phone').text
        work_time = soup.find('div', class_='footer__weekdays').text
        article = {
            'name': 'NEO',
            'content': content,
            'address': address,
            'telephone': telephone,
            'work-time': work_time,
        }
        article_list_clinic.append(article)
        doctors = soup.findAll('div', class_='specialists__card card ')
        for d in doctors:
            doc_name = d.find('span', class_='specialists__name card__name').text
            doc_content = d.find('p').text
            article = {
                'name': doc_name,
                'content': doc_content
            }
            article_list_doc.append(article)
        r = requests.get('https://prodoctorov.ru/kazan/lpu/45057-medicinskiy-centr-neo/price/#tab-content')
        soup = BeautifulSoup(r.content, features='xml')
        services = soup.find_all('div', class_='b-clinic-prices__list-item')
        for s in services:
            service_name = s.find('div', class_='b-clinic-prices__key b-clinic-prices__key_js_full-prices').text
            service_price = s.find('div', class_='b-clinic-prices__value b-text-unit b-text-unit_weight_medium').text
            article = {
                'name': service_name,
                'price': service_price
            }
            article_list_ser.append(article)
        return save_function(article_list_ser, article_list_doc, article_list_clinic)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)


def erdamed_rss():
    article_list_doc = []
    article_list_ser = []
    article_list_clinic = []
    try:
        driver = webdriver.Edge()
        driver.get('https://erdamed.ru/')
        content = driver.find_element(By.CLASS_NAME, 'main__banner--text').find_element(By.TAG_NAME, 'p').text
        address = driver.find_element(By.CLASS_NAME, 'address').find_element(By.TAG_NAME, 'a').text
        telephone = driver.find_element(By.CLASS_NAME, 'phone').find_element(By.TAG_NAME, 'a').text
        work_time = driver.find_element(By.CLASS_NAME, 'phone__text').text.replace('\u2060', '')
        article = {
            'name': 'ERDA',
            'content': content,
            'address': address,
            'telephone': telephone,
            'work-time': work_time,
        }
        article_list_clinic.append(article)
        driver.get('https://erdamed.ru/personal/')
        doctors = driver.find_elements(By.CLASS_NAME, 'main__doctor--cart')
        for d in doctors:
            doc_name = d.find_element(By.CLASS_NAME, 'main__doctor--name').text
            doc_content = d.find_element(By.CLASS_NAME, 'post').text
            article = {
                'name': doc_name,
                'content': doc_content
            }
            article_list_doc.append(article)
        r = requests.get('https://prodoctorov.ru/kazan/lpu/45395-erda-medicine/price/#tab-content')
        soup = BeautifulSoup(r.content, features='xml')
        services = soup.find_all('div', class_='b-lpu-services__service')
        for s in services:
            service_name = s.find('div', class_='b-lpu-services__service-name ui-text ui-text_body-1').text
            service_price = s.find('div', class_='b-lpu-services__price ui-text ui-text_subtitle-1 '
                                                 'ui-text_color_black text-right').text
            article = {
                'name': service_name,
                'price': service_price
            }
            article_list_ser.append(article)
        return save_function(article_list_ser, article_list_doc, article_list_clinic)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)


def vaelstom_rss():
    article_list_doc = []
    article_list_ser = []
    article_list_clinic = []
    try:
        r = requests.get('https://vaelstom.ru/')
        soup = BeautifulSoup(r.content, features='xml')
        content = soup.find('div', class_='col-lg-5 col-xl-4 offset-xl-1 services-wrapper').find('p').text
        address = soup.find('div', class_='header-address d-flex align-items-center').find('div').text
        telephone = soup.find('a', class_='d-flex align-items-center phone').text
        work_time = soup.find('div', class_='header-address d-flex align-items-center').find('div').text
        article = {
            'name': 'VaelStom',
            'content': content,
            'address': address,
            'telephone': telephone,
            'work-time': work_time,
        }
        article_list_clinic.append(article)
        doctors = soup.findAll('div', class_='team-card-inner')
        for d in doctors:
            try:
                doc_content = d.find('div', class_='team-card-position').text
            except Exception as e:
                doc_content = ""
            doc_name = d.find('div', class_='team-card-name').text.replace(doc_content, '')
            article = {
                'name': doc_name,
                'content': doc_content
            }
            article_list_doc.append(article)
        services = soup.findAll('div', class_='service-item')
        for s in services:
            service_name = s.find('a').text.replace(s.find('div', class_='service-item-number').text, '')
            article = {
                'name': service_name,
                'price': ""
            }
            article_list_ser.append(article)
        return save_function(article_list_ser, article_list_doc, article_list_clinic)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)


def cord_rss():
    article_list_doc = []
    article_list_ser = []
    article_list_clinic = []
    try:
        driver = webdriver.Edge()
        driver.get('https://kord-klinika.ru/')
        address = driver.find_element(By.CLASS_NAME, 'address').find_element(By.CLASS_NAME, 'footer__top-desc').text
        telephone = driver.find_element(By.CLASS_NAME, 'tel').find_element(By.CLASS_NAME, 'footer__top-desc').text
        work_time = driver.find_element(By.CLASS_NAME, 'work').find_element(By.CLASS_NAME, 'footer__top-desc').text
        content = driver.find_element(By.CLASS_NAME, 'blockquote__txt').text
        article = {
            'name': 'Корд-Клиника',
            'address': address,
            'telephone': telephone,
            'work-time': work_time,
            'content': content
        }
        article_list_clinic.append(article)
        r = requests.get('https://prodoctorov.ru/kazan/lpu/50986-kord-klinika/vrachi/#tab-content')
        soup = BeautifulSoup(r.content, features='xml')
        doctors = soup.find_all('div', class_="b-doctor-card__top")
        for d in doctors:
            article = {
                'name': d.find('span', class_='b-doctor-card__name-surname').text,
                'content': d.find('div', class_='b-doctor-card__spec').text
            }
            article_list_doc.append(article)
        r = requests.get('https://prodoctorov.ru/kazan/lpu/50986-kord-klinika/price/#tab-content')
        soup = BeautifulSoup(r.content, features='xml')
        services = soup.find_all('div', class_='b-clinic-prices__list-item')
        for s in services:
            article = {
                'name': s.find('div', class_="b-clinic-prices__key b-clinic-prices__key_js_full-prices").text,
                'price': s.find('div', class_="b-clinic-prices__value b-text-unit b-text-unit_weight_medium").text
            }
            article_list_ser.append(article)
        return save_function(article_list_ser, article_list_doc, article_list_clinic)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)


def save_function(article_list_ser, article_list_doc, article_list_clinic):
    for article in article_list_clinic:
        article['name'] = article['name'].replace('\n', '').strip()
        article['name'] = article['name'].replace('\t', '').strip()
        article['content'] = article['content'].replace('\n', '').strip()
        article['content'] = article['content'].replace('\t', '').strip()
        article['address'] = article['address'].replace('\n', '').strip()
        article['address'] = article['address'].replace('\t', '').strip()
        article['telephone'] = article['telephone'].replace('\n', '').strip()
        article['telephone'] = article['telephone'].replace('\t', '').strip()
        article['work-time'] = article['work-time'].replace('\n', '').strip()
        article['work-time'] = article['work-time'].replace('\t', '').strip()
        try:
            Clinics.objects.create(
                ClinicName=article['name'],
                ClinicContent=article['content'],
                ClinicAddress=article['address'],
                ClinicTelephone=article['telephone'],
                ClinicWork_time=article['work-time']
            )
        except Exception as e:
            print('failed at latest_article is none')
            print(e)
            break
    pk = Clinics.objects.last().id
    for article in article_list_doc:
        article['name'] = article['name'].replace('\n', '').strip()
        article['name'] = article['name'].replace('\t', '').strip()
        article['content'] = article['content'].replace('\n', '').strip()
        article['content'] = article['content'].replace('\t', '').strip()
        try:
            Doctor.objects.create(
                DoctorClinic=Clinics.objects.last(),
                DoctorName=article['name'],
                DoctorContent=article['content'],
            )
        except Exception as e:
            print('failed at article_doctor is none')
            print(e)
            break
    for article in article_list_ser:
        article['name'] = article['name'].replace('\n', '').strip()
        article['name'] = article['name'].replace('\t', '').strip()
        article['price'] = article['price'].replace('\n', '').strip()
        article['price'] = article['price'].replace('\t', '').strip()
        try:
            Services.objects.create(
                ServiceClinic=Clinics.objects.last(),
                ServiceName=article['name'],
                ServicePrice=article['price'],
            )
        except Exception as e:
            print('failed at article_service is none')
            print(e)
            break

    return print('All right!')


