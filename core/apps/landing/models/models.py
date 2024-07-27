from django.db import models

from apps.landing.models.entity import ColorFontEnum


class Site(models.Model):
    whatsapp = models.CharField("WhatsApp", max_length=16)
    phone = models.CharField("Phone", max_length=15)

    def __str__(self):
        return "Site landing"


class MainScreen(models.Model):
    title = models.CharField("Title", max_length=100)
    text = models.TextField(
        "Description", blank=True, help_text="Above the title"
    )
    subtext = models.TextField(
        "Substext", blank=True, help_text="Under the title"
    )
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, related_name="main_screen"
    )

    class Meta:
        verbose_name = "Main Screen"
        verbose_name_plural = "Main Screen"

    def __str__(self):
        return "Main screen"


class Service(models.Model):
    name = models.CharField("Service name", max_length=100)
    font_color = models.ForeignKey("ColorFont", on_delete=models.PROTECT)
    discount_message = models.CharField(
        "Discount message", max_length=100, blank=True
    )
    image = models.ImageField("Service image", upload_to="service/")
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="services"
    )

    def __str__(self):
        return f"Service {self.name}"

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"


class ServiceDetail(models.Model):
    service = models.OneToOneField(
        Service, on_delete=models.CASCADE, related_name="service_detail"
    )
    quality_title = models.CharField("Service quality title", max_length=100)
    quality_text = models.TextField("Service quality text")

    def __str__(self):
        return f"Details for service {self.service.name}"

    class Meta:
        verbose_name = "Service detail"
        verbose_name_plural = "Service details"


class Advantage(models.Model):
    title = models.CharField("Advantage title", max_length=100)
    text = models.TextField("Advantage description")
    service = models.ForeignKey(
        ServiceDetail, on_delete=models.CASCADE, related_name="advantage"
    )

    class Meta:
        verbose_name = "Advantage"
        verbose_name_plural = "Advantages"

    def __str__(self):
        return f"Advantage {self.title}"


class About(models.Model):
    title = models.CharField("About title", max_length=100)
    text = models.TextField("About text")
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, related_name="about"
    )

    def __str__(self):
        return "About"

    class Meta:
        verbose_name = "About"
        verbose_name_plural = "About"


class AboutBlock(models.Model):
    first_title = models.CharField("Title 1", max_length=100)
    first_description = models.TextField("Subtext for Title 1")
    second_title = models.CharField("Title 2", max_length=100)
    second_description = models.TextField("Subtext for Title 2")
    about = models.ForeignKey(
        About, on_delete=models.CASCADE, related_name="blocks"
    )


class OurResultsPhoto(models.Model):
    image = models.ImageField("Result photo", upload_to="results/")
    result = models.ForeignKey(
        "OurResults",
        on_delete=models.CASCADE,
        related_name="result_photos",
    )

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"


class OurResults(models.Model):
    description = models.TextField("Results description")
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, related_name="results"
    )

    def __str__(self):
        return "Our results"

    class Meta:
        verbose_name = "Our results"
        verbose_name_plural = "Our results"


class ColorFont(models.Model):
    COLORS = (
        (ColorFontEnum.black.value, "black"),
        (ColorFontEnum.white.value, "white"),
    )
    color = models.CharField(
        "Color", choices=COLORS, max_length=16, unique=True
    )

    def __str__(self):
        return f"{self.get_color_display()}"


class Footer(models.Model):
    email = models.EmailField("Email")
    operating_mode = models.CharField("Operating mode", max_length=32)
    address = models.CharField("company address", max_length=64)
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, related_name="footer"
    )

    def __str__(self):
        return "Footer"

    class Meta:
        verbose_name = "Footer"
        verbose_name_plural = "Footer"
