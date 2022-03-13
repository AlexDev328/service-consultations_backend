import base64
import io
import secrets
from random import choice
from PIL import Image
from django.db.models import Q
from django.core.exceptions import *
from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework import status, mixins
from rest_framework.decorators import api_view



from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, )
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .forms import UploadFileForm
from .models import UserProfile, User, Photo, Consultation, AuthCode
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import UserProfileSerializer, ConsultationSerializer


class UserProfileListCreateView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', False)
        if not pk:
            instance = UserProfile.objects.get(user=request.user)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            super().retrieve(request, *args, **kwargs)





class ConsultationView(ModelViewSet):
    permission_classes_by_action = {'retrieve': [AllowAny],
                                    'patch': [AllowAny]}
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer

    def get_queryset(self):
        if self.action == 'list' and self.request.user:
            return Consultation.objects.filter(Q(consultant__user=self.request.user) | Q(status=0))
        else:
            return Consultation.objects.all()




def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Photo(img=request.FILES['img'])
            instance.save()
            return Response(status=201)
    else:
        form = UploadFileForm()
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


def get_image_from_data_url(data_url, resize=True, base_width=600):
    # getting the file format and the necessary dataURl for the file
    img_format, dataurl = data_url.split(';base64,')
    # file name and extension
    filename, extension = secrets.token_hex(20), img_format.split('/')[-1]
    # generating the contents of the file
    file = ContentFile(base64.b64decode(dataurl), name=f"{filename}.{extension}")
    # resizing the image, reducing quality and size
    if resize:
        # opening the file with the pillow
        image = Image.open(file)
        # using BytesIO to rewrite the new content without using the filesystem
        image_io = io.BytesIO()
        # resize
        w_percent = (base_width / float(image.size[0]))
        h_size = int((float(image.size[1]) * float(w_percent)))
        image = image.resize((base_width, h_size), Image.ANTIALIAS)
        # save resized image
        image.save(image_io, format=extension)
        # generating the content of the new image
        file = ContentFile(image_io.getvalue(), name=f"{filename}.{extension}")
    # file and filename
    return file


def get_dataurl_from_image(file, resize, base_width=300):
    with open(file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        print(encoded_string)
        return ('data:image/png;base64,' + str(encoded_string)[2:-1])
    return ''


'''def upload_conclusion(request):
    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        cons_text = request.POST.get('cons_text')
        final = request.POST.get('final')

        if final == "True":
            final = True
        else:
            final = False
        try:
            conclusion = Conclusion.objects.get(application=Application.objects.get(pk=app_id))
            conclusion.cons_text = cons_text
            conclusion.final = final
        except ObjectDoesNotExist:
            conclusion = Conclusion.objects.create(application=Application.objects.get(pk=app_id), cons_text=cons_text,
                                                   final=final)
        parsed_images = json.loads(request.POST.get("imgs"))
        conclusion.save()
        # не загружаем уже загруженные изображения( т.к. они у нс не удаляются на фронте, необходимо отсеивать уже существующие)
        img_count = Photo.objects.filter(conclusion=conclusion).count()
        for i in range(img_count, len(parsed_images)):
            instance = Photo(img=get_image_from_data_url(parsed_images[i], False), conclusion_id=conclusion.pk)
            instance.save()
    return HttpResponse(status=status.HTTP_201_CREATED)'''

from string import ascii_lowercase, digits


def generate_random_username(length=16, chars=ascii_lowercase + digits, split=4, delimiter='-'):
    username = ''.join([choice(chars) for i in range(length)])
    if split:
        username = delimiter.join([username[start:start + split] for start in range(0, len(username), split)])

    try:
        User.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except User.DoesNotExist:
        return username


from .token_generator import get_tokens_for_user


@api_view(['POST'])
def create_application(request):
    if request.method == 'POST':
        data = request.data
        userdata = data.get('user')
        print(data)
        try:
            current_user_profile = UserProfile.objects.get(user_inner_id=userdata['id'])
            auth_code = current_user_profile.auth_code.regenerate_code()
        except UserProfile.DoesNotExist:
            user = User.objects.create_user(username=generate_random_username())
            user.first_name = userdata['personName']['name']
            user.last_name = userdata['personName']['surnames']
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            auth_code = AuthCode.objects.create()
            current_user_profile = UserProfile.objects.create(user=user, user_inner_id=userdata['id'], auth_code=auth_code)
            current_user_profile.save()

        res = Consultation.objects.create(insigator=current_user_profile, data=data['params'])
        res.save()
        serializer = ConsultationSerializer(res)
        print(serializer)
        content = {'link': f'{settings.CONSULTATIONS_HOST}consultation/{res.id}?auth_code={auth_code.auth_code}'}
        return Response(status=status.HTTP_201_CREATED, data=content)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def aprove_application(request, id):
    consultation = Consultation.objects.get(id=id)
    if consultation.consultant is None or consultation.consultant.user == request.user:
        consultation.consultant = UserProfile.objects.get(user=request.user)
        consultation.status = 1
        consultation.save()
        return Response(status=status.HTTP_200_OK, data=ConsultationSerializer(consultation).data)
    return Response(status=status.HTTP_208_ALREADY_REPORTED)



@api_view(['GET'])
def auth_by_link(request, auth_code):
    user = UserProfile.objects.get(auth_code__auth_code=auth_code)
    if user:
        tokens = get_tokens_for_user(user.user)
        return Response(status=status.HTTP_200_OK, data=tokens)
    return Response(status=status.HTTP_208_ALREADY_REPORTED)