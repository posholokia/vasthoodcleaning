from apps.landing.models.entity import (
    ColorFontEnum,
    MainScreenEntity,
    ServiceEntity,
    FontColorEntity,
    ServiceDetailEntity,
    AdvantageEntity,
    AboutEntity,
    AboutBlockEntity,
    ResultPhotoEntity,
    ResultEntity,
    FooterEntity,
    FAQEntity,
    SiteEntity,
)
from django.db import models


class Site(models.Model):
    whatsapp = models.CharField("WhatsApp", max_length=256)
    phone = models.CharField("Phone", max_length=32)

    def __str__(self):
        return "Site landing"

    def to_entity(self) -> SiteEntity:
        about = self.about.to_entity() if hasattr(self, "about") else None
        results = (
            self.results.to_entity() if hasattr(self, "results") else None
        )
        main_screen = (
            self.main_screen.to_entity() if hasattr(self, "footer") else None
        )
        footer = self.footer.to_entity() if hasattr(self, "footer") else None
        return SiteEntity(
            id=self.id,
            whatsapp=self.whatsapp,
            phone=self.phone,
            about=about,
            results=results,
            services=[s.to_entity() for s in self.services.all()],
            main_screen=main_screen,
            faq=[f.to_entity() for f in self.faq.all()],
            footer=footer,
        )


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

    def to_entity(self) -> MainScreenEntity:
        return MainScreenEntity(
            id=self.id,
            title=self.title,
            text=self.text,
            subtext=self.subtext,
        )


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

    def to_entity(self) -> ServiceEntity:
        return ServiceEntity(
            id=self.id,
            name=self.name,
            font_color=self.font_color.to_entity(),
            image=str(self.image),
            discount_message=self.discount_message,
        )

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

    def to_entity(self) -> ServiceDetailEntity:
        return ServiceDetailEntity(
            id=self.id,
            service=self.service.to_entity(),
            quality_title=self.quality_title,
            quality_text=self.quality_text,
            advantage=[a.to_entity() for a in self.advantage.all()],
        )

    class Meta:
        verbose_name = "Service detail"
        verbose_name_plural = "Service details"


class Advantage(models.Model):
    title = models.CharField("Advantage title", max_length=100)
    text = models.TextField("Advantage description")
    service = models.ForeignKey(
        ServiceDetail, on_delete=models.CASCADE, related_name="advantage"
    )

    def __str__(self):
        return f"Advantage {self.title}"

    def to_entity(self) -> AdvantageEntity:
        return AdvantageEntity(
            id=self.id,
            title=self.title,
            text=self.text,
        )

    class Meta:
        verbose_name = "Advantage"
        verbose_name_plural = "Advantages"


class About(models.Model):
    title = models.CharField("About title", max_length=100)
    text = models.TextField("About text")
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, related_name="about"
    )

    def __str__(self):
        return "About"

    def to_entity(self) -> AboutEntity:
        return AboutEntity(
            id=self.id,
            title=self.title,
            text=self.text,
            blocks=[b.to_entity() for b in self.blocks.all()],
        )

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

    def to_entity(self) -> AboutBlockEntity:
        return AboutBlockEntity(
            id=self.id,
            first_title=self.first_title,
            first_description=self.first_description,
            second_title=self.second_title,
            second_description=self.second_description,
        )


class OurResultsPhoto(models.Model):
    image = models.ImageField("Result photo", upload_to="results/")
    result = models.ForeignKey(
        "OurResults",
        on_delete=models.CASCADE,
        related_name="result_photos",
    )

    def to_entity(self) -> ResultPhotoEntity:
        return ResultPhotoEntity(
            id=self.id,
            image=str(self.image),
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

    def to_entity(self) -> ResultEntity:
        return ResultEntity(
            id=self.id,
            description=self.description,
            result_photos=[p.to_entity() for p in self.result_photos.all()],
        )

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

    def to_entity(self) -> FontColorEntity:
        return FontColorEntity(
            id=self.id,
            color=ColorFontEnum(self.color),
        )


class Footer(models.Model):
    email = models.EmailField("Email")
    operating_mode = models.CharField("Operating mode", max_length=32)
    address = models.CharField("company address", max_length=64)
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, related_name="footer"
    )

    def __str__(self):
        return "Footer"

    def to_entity(self) -> FooterEntity:
        return FooterEntity(
            id=self.id,
            email=self.address,
            operating_mode=self.address,
            address=self.address,
        )

    class Meta:
        verbose_name = "Footer"
        verbose_name_plural = "Footer"


class FAQ(models.Model):
    question = models.TextField("Question")
    answer = models.TextField("Answer")
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="faq"
    )

    def __str__(self):
        return "FAQ"

    def to_entity(self) -> FAQEntity:
        return FAQEntity(
            id=self.id,
            question=self.question,
            answer=self.answer,
        )

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"
