from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
from django.db import models
from ordered_model.models import OrderedModel


# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, email=None, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not username:
            raise ValueError('username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, email=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(username, password, email, **extra_fields)

    def create_superuser(self, username, password=None, email=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, email, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    App base User Class.
    Email and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
        help_text=_('Valor requirido. Somente letras e dígitos.'),
        validators=[username_validator],
        error_messages={
            'unique': _('Já existe um usuario com este username.')
        },
    )
    first_name = models.CharField(_('Nome'), max_length=150)
    last_name = models.CharField(_('Sobrenomes'), max_length=150, blank=True)
    email = models.EmailField(_('Email'), unique=True)
    phone = models.CharField(_('Phone number'), max_length=50, blank=True)
    cpf_cnpj = models.CharField('CFP/CNPJ', max_length=50, blank=True)
    address = models.CharField(_('Address'), max_length=200, blank=True)
    cep = models.CharField('CEP', max_length=10, blank=True)
    picture = models.ImageField(_('Arquivo foto'), upload_to='images/', null=True)

    USER_TYPE_CHOICES = (
        ('admin', 'Administrador BD'),
        ('gestor', 'Gestor WFW'),
        ('staff', 'Apoiador'),
        ('giver', 'Doadoar'),
        ('beneficiary', 'Beneficiario')
    )

    user_type = models.CharField(_('Tipo de Usuário'), max_length=20, blank=True,
                                 choices=USER_TYPE_CHOICES)

    is_staff = models.BooleanField(
        _('staff status'),
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
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s' % self.first_name
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Foto(OrderedModel):
    descricao = models.CharField(_('Description'), max_length=150)
    imagefile = models.ImageField(_('Image File'), upload_to='images/', null=True)
    evento = models.ForeignKey('Evento', on_delete=models.PROTECT)
    slug = models.SlugField(unique=True)

    order_with_respect_to = 'evento'

    class Meta(OrderedModel.Meta):
        ordering = ('order', )

    def __str__(self):
        return self.descricao


class Item(models.Model):
    descricao = models.CharField(_('Description'), max_length=150)

    ITEM_TYPE_CHOICES = (
        ('dinheiro', 'Valor Monetário'),
        ('produto', 'Produto'),
    )

    item_type = models.CharField(_('Tipo de item'), max_length=20, blank=True,
                                 choices=ITEM_TYPE_CHOICES)

    def __str__(self):
        return self.descricao


class Evento(OrderedModel):
    descricao = models.CharField(_('Description'), max_length=150)
    data = models.DateField(_('Date'))
    slug = models.SlugField(unique=True)

    EVENTO_STATUS_CHOICES = (
        ('planejamento', 'Em planejamento'),
        ('pronto', 'Pronto para realização'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
        ('adiado', 'Adiado')
    )

    status = models.CharField(_('Tipo de item'), max_length=20, blank=True,
                              choices=EVENTO_STATUS_CHOICES)

    def __str__(self):
        return self.descricao


class Depoimento(models.Model):
    texto = models.CharField(_('Texto'), max_length=500)
    data = models.DateField(_('Date'))
    usuario = models.ForeignKey('User', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.data}: {self.texto}'
