
import os
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.db import models

# Create your models here.

from typing import Optional
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,UserManager
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError


class DepartmentModel(models.Model):

    number = models.AutoField(primary_key=True)

    name = models.CharField(
        _("Name"),
        max_length=150,
        unique=True
    )


    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        db_table = 'department'

    def __str__(self) -> str:
        return self.name

class User(AbstractBaseUser):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    # username_validator = UnicodeUsernameValidator()
    u_id = models.AutoField(primary_key=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        # validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    
    f_name = models.CharField(_('First name'), max_length=150, blank=False)
    # m_name = models.CharField(_('Middle name'), max_length=150, blank=False)
    l_name = models.CharField(_('Last name'), max_length=150, blank=False)
    email = models.EmailField(_('Email address'), null=True,unique=True)

    # manager = models.ForeignKey('self',verbose_name=_("Manager"),on_delete = models.PROTECT,null=True,blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_superuser = models.BooleanField(
        _('is_superusers'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    GENDER=(
        ('male',_('male')),
        ('female',_('female'))
    )
    
    gander = models.CharField(
        _("Gander"),
        max_length=20,
        choices=GENDER,
    )
    
    Department =models.ForeignKey(
        DepartmentModel,
        verbose_name=_("Department"),
        on_delete = models.CASCADE,
        null=True
    )

    
    STATUS=(
        ('aware',_('aware')),
        ('unaware',_('unaware'))
    )
    phishing_awareness = models.CharField(
        _("Phishing Awareness"),
        max_length=15,
        choices=STATUS,
        default="aware"
    )

    last_update = models.DateTimeField(
        _("last_update"),
        blank=True,null=True

    )
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    
    # def __str__(self):
    #     return self.f_name +self.l_name
    

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'User'

class Url(models.Model):
    url_id = models.AutoField(primary_key=True)

    name = models.CharField(
        _("Name"),
        max_length=30,
    )

    description = models.CharField(
        _("Description"),
        max_length=150,
        unique=True
    )

    TYPE=(
        ('secure',_('secure')),
        ('unsecure',_('unsecure'))
    )
    type = models.CharField(
        _("Type"),
        max_length=15,
        choices=TYPE,
    )
    
    TEMPLATES=(
        ('None',_('None')),
        ('fb',_('Facebook')),
        ('sbl',_('SPL')),
        ('unv',_('University')),
    )
    template = models.CharField(
        _("Type"),
        max_length=15,
        choices=TEMPLATES,
        null=True
    )
    class Meta:
        verbose_name = _('Url')
        verbose_name_plural = _('Urls')
        db_table = 'Url'


    def __str__(self) -> str:
        return self.name

class TrainingPackage(models.Model):
    t_id = models.AutoField(primary_key=True)

    Name = models.CharField(
        _("Name"),
        max_length=150,
        default="1",
        unique=True
    )

    description = models.CharField(
        _("Description"),
        max_length=150,
    )

    
    type = models.CharField(
        _("Type"),
        max_length=50,
    )

    train_file = models.FileField(
        upload_to='uploads/',
        verbose_name=_('Training File'),
        blank=True,null=True
        )

    
    class Meta:
        verbose_name = _('Training Package')
        verbose_name_plural = _('Training Packages')
        db_table = 'TrainingPackage'

    def __str__(self) -> str:
        return self.Name

class SurfingModel(models.Model):
    URL_ID =models.ForeignKey(
        Url,
        verbose_name=_("URl"),
        on_delete = models.CASCADE,
        null=True
    )

    U_ID =models.ForeignKey(
        User,
        verbose_name=_("User"),
        on_delete = models.CASCADE,
        null=True
    )
    class Meta:
        verbose_name = _('Surfing')
        verbose_name_plural = _('Surfing')
        db_table = 'Surfing'

class SendingURlsModel(models.Model):
    URL_ID =models.ForeignKey(
        Url,
        verbose_name=_("URl"),
        on_delete = models.CASCADE,
        null=True
    )

    U_ID =models.ForeignKey(
        User,
        verbose_name=_("User"),
        on_delete = models.CASCADE,
        null=True,blank=True
    )
    
    Department =models.ForeignKey(
        DepartmentModel,
        verbose_name=_("Department"),
        on_delete = models.CASCADE,
        null=True,blank=True
    )

    time = models.DateTimeField(
        _("Sending Time"),
        default=timezone.now(),
    )

    SENDTO=(
        ('user',_('user')),
        ('department',_('department')),
        ('all_users',_('All users'))

    )
    send_to = models.CharField(
        _("Send To"),
        max_length=15,
        choices=SENDTO,
    )
    email_text = models.TextField(
        _("email_text"),
        null=True,
    )

    class Meta:
        verbose_name = _('SendingURls')
        verbose_name_plural = _('SendingURls')
        db_table = 'SendingURls'

class SendingTrainingModel(models.Model):
    Train_ID =models.ForeignKey(
        TrainingPackage,
        verbose_name=_("Training Package"),
        on_delete = models.CASCADE,
        null=True
    )

    U_ID =models.ForeignKey(
        User,
        verbose_name=_("User"),
        on_delete = models.CASCADE,
        null=True,blank=True
    )
    
    Department =models.ForeignKey(
        DepartmentModel,
        verbose_name=_("Department"),
        on_delete = models.CASCADE,
        null=True,blank=True
    )

    time = models.DateTimeField(
        _("Sending Time"),
        default=timezone.now(),
    )

    SENDTO=(
        ('user',_('user')),
        ('department',_('department')),
        ('all_users',_('All users'))
    )
    send_to = models.CharField(
        _("Send To"),
        max_length=15,
        choices=SENDTO,
    )
    email_text = models.TextField(
        _("email_text"),
        null=True,
    )
    

    class Meta:
        verbose_name = _('Sending TrainingPackage ')
        verbose_name_plural = _('Sending TrainingPackages')
        db_table = 'SendingTrainingPackage'

def send_email(recipient_list,message,subject):
    import smtplib
    from email.mime.text import MIMEText
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpserver.ehlo()
    smtpserver.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    sent_from = EMAIL_HOST_USER
    sent_to = recipient_list  #  Send it to self (as test)
    email_text = message
    msg = MIMEText(email_text)
    msg['Subject'] = subject

    # Convert the message to a string and send it
    smtpserver.sendmail(sent_from, sent_to, msg.as_string())
    smtpserver.quit()

def send_email_with_file(recipient_list,message,subject,attachment_path):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

    smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpserver.ehlo()
    smtpserver.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

    sent_from = EMAIL_HOST_USER
    sent_to = recipient_list
    msg = MIMEMultipart()
    msg['From'] = sent_from
    msg['To'] = ', '.join(sent_to)
    msg['Subject'] = subject

    # Attach body text
    msg.attach(MIMEText(message, 'plain'))

    # Attach the file
    attachment = open(attachment_path, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment_path)}")
    msg.attach(part)

    # Convert the message to a string and send it
    smtpserver.sendmail(sent_from, sent_to, msg.as_string())

    smtpserver.quit()

from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

@receiver(post_save, sender=SendingURlsModel)
def send_throw_email(sender, instance, created, **kwargs):
    send_to=instance.send_to
    if send_to=="user":
        email=instance.U_ID.email
        if instance.URL_ID.type=='unsecure':
            url='http://127.0.0.1:8000/'+instance.URL_ID.description
        else:
            url={instance.URL_ID.description}
        subject = f'Link Details {instance.time.strftime("%Y-%m-%d %H:%M:%S")}'
        message = f'{instance.email_text}  \n {url} \n Thank You'
        recipient_list = [email]
        send_email(recipient_list,message,subject)

        from django.db.models import Q
    
        user_last_update=instance.U_ID.last_update
        user_dep=instance.U_ID.Department
        pre_data=SendingURlsModel.objects.filter(
            Q(time__gt=user_last_update,U_ID=instance.U_ID) | Q(time__gt=user_last_update,Department=user_dep)
            )
        
        if len(pre_data)>=3:
            instance.U_ID.last_update=timezone.now()
            instance.U_ID.phishing_awareness="aware"
            instance.U_ID.save()


    elif send_to=="department":
        emails=instance.Department.user_set.filter(Department=instance.Department).values_list('email',flat=True)
        print(list(emails),"emialisemialis")
        if instance.URL_ID.type=='unsecure':
            url='http://127.0.0.1:8000/'+instance.URL_ID.description
        else:
            url={instance.URL_ID.description}
        subject = f'Link Details {instance.time.strftime("%Y-%m-%d %H:%M:%S")}'
        message = f'{instance.email_text}  \n {url} \n Thank You'
        recipient_list = emails
        send_email(recipient_list,message,subject)

        from django.db.models import Q
        users=instance.Department.user_set.filter(Department=instance.Department)

        for user in users:
            user_dep=user.Department
            user_last_update=user.last_update
            pre_data=SendingURlsModel.objects.filter(
            Q(time__gt=user_last_update,U_ID=user) | Q(time__gt=user_last_update,Department=user_dep)
            )
            if len(pre_data)>=3:
                user.last_update=timezone.now()
                user.phishing_awareness="aware"
                user.save()
            print(pre_data,"pre_datapre_datapre_data",len(pre_data))

    elif send_to=="all_users":
        emails = User.objects.filter(is_superuser=False, email__isnull=False).values_list('email', flat=True)
        print(list(emails),"emialisemialis")
        if instance.URL_ID.type=='unsecure':
            url='http://127.0.0.1:8000/'+instance.URL_ID.description
        else:
            url={instance.URL_ID.description}
        subject = f'Link Details {instance.time.strftime("%Y-%m-%d %H:%M:%S")}'
        message = f'{instance.email_text}  \n {url} \n Thank You'
        recipient_list = emails
        
        send_email(recipient_list,message,subject)

        from django.db.models import Q
        users = User.objects.filter(is_superuser=False, email__isnull=False)

        for user in users:
            user_dep=user.Department
            user_last_update=user.last_update
            pre_data=SendingURlsModel.objects.filter(
            Q(time__gt=user_last_update,U_ID=user) | Q(time__gt=user_last_update,Department=user_dep)
            )
            if len(pre_data)>=3:
                user.last_update=timezone.now()
                user.phishing_awareness="aware"
                user.save()
            print(pre_data,"pre_datapre_datapre_data",len(pre_data))

@receiver(post_save, sender=SendingTrainingModel)
def send_throw_email(sender, instance, created, **kwargs):
    send_to=instance.send_to
    if send_to=="user":
        email=instance.U_ID.email
        subject = f'TrainingPackage {instance.time.strftime("%Y-%m-%d %H:%M:%S")}'
        message = f'{instance.email_text} \n Thank You'
        recipient_list = [email]
        attachment_path = instance.Train_ID.train_file.path
        
        send_email_with_file(recipient_list,message,subject,attachment_path)

    elif send_to=="department":
        emails=instance.Department.user_set.filter(Department=instance.Department,phishing_awareness="unaware").values_list('email',flat=True)
        print(list(emails),"emialisemialis")
        subject = f'TrainingPackage {instance.time.strftime("%Y-%m-%d %H:%M:%S")}'
        message = f'{instance.email_text} \n Thank You'
        recipient_list = emails
        attachment_path = instance.Train_ID.train_file.path
        send_email_with_file(recipient_list,message,subject,attachment_path)
    
    elif send_to=="all_users":
        emails=User.objects.filter(is_superuser=False,phishing_awareness="unaware").values_list('email',flat=True)
        print(list(emails),"emialisemialis")
        subject = f'TrainingPackage {instance.time.strftime("%Y-%m-%d %H:%M:%S")}'
        message = f'{instance.email_text} \n Thank You'
        recipient_list = emails
        attachment_path = instance.Train_ID.train_file.path

        send_email_with_file(recipient_list,message,subject,attachment_path)
