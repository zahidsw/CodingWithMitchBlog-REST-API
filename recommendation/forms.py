from django import forms

from recommendation.models import Recommendation


class CreateBlogPostForm(forms.ModelForm):

	class Meta:
		model = Recommendation
		fields = ['sku','artikelNr1','artikelNr2', 'statusCode' ,'statusText' ,'saisonRetourenCode','saisonRetourenText','saisonCode','saisonText','geschlechtCode','geschlechtText','rayonCode','rayonText','warenArtCode','warenArtText','wuCode','wuText','waCode','warenGruppe','alterCode','farbe','material','bezeichnung','pictureName','picturePathLocal','kollektion','comCode' ,'lieferant','eKchf','eti','vp','groessenCode' ,'groessen','zlQty' ,'productId','published' ,'categories' ,'productName','shortDescription','fullDescription','flag']


class UpdateBlogPostForm(forms.ModelForm):

	class Meta:
		model = Recommendation
		fields = ['sku','artikelNr1','artikelNr2', 'statusCode' ,'statusText' ,'saisonRetourenCode','saisonRetourenText','saisonCode','saisonText','geschlechtCode','geschlechtText','rayonCode','rayonText','warenArtCode','warenArtText','wuCode','wuText','waCode','warenGruppe','alterCode','farbe','material','bezeichnung','pictureName','picturePathLocal','kollektion','comCode' ,'lieferant','eKchf','eti','vp','groessenCode' ,'groessen','zlQty' ,'productId','published' ,'categories' ,'productName','shortDescription','fullDescription','flag']

	def save(self, commit=True):
		blog_post = self.instance
		blog_post.title = self.cleaned_data['title']
		blog_post.body = self.cleaned_data['body']

		if self.cleaned_data['image']:
			blog_post.image = self.cleaned_data['image']

		if commit:
			blog_post.save()
		return blog_post