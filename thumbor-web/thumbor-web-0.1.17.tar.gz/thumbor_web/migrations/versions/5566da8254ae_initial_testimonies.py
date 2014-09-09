"""initial testimonies

Revision ID: 5566da8254ae
Revises: 53ef6444c12
Create Date: 2014-09-03 17:24:43.100849

"""

# revision identifiers, used by Alembic.
revision = '5566da8254ae'
down_revision = '53ef6444c12'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table


def upgrade():
    testimonials_table = table(
        'testimonials',
        sa.Column('id', sa.Integer()),
        sa.Column('sender_name', sa.String(length=200)),
        sa.Column('email', sa.String(length=255)),
        sa.Column('company_name', sa.String(length=200)),
        sa.Column('company_url', sa.String(length=2000)),
        sa.Column('company_logo', sa.String(length=2000)),
        sa.Column('approved', sa.Boolean),
        sa.Column('summary', sa.Text()),
        sa.Column('text', sa.Text()),
        sa.Column('order', sa.Integer())
    )

    op.bulk_insert(
        testimonials_table,
        [
            {
                "sender_name": "Bernardo Heynemann",
                "email": "heynemann@gmail.com",
                "company_name": "properati",
                "company_url": "http://www.properati.com.ar/",
                "company_logo": "/static/images/logos/testimonials-properati.png",
                "approved": True,
                "summary":
                    "Properati is using thumbor to generate several different sizes of their properties photos, "
                    "using smart cropping to get the best possible thumbnails.",
                "text":
                    "Thumbor made our lives better.\nAt Properati.com.ar we care a lot about user experience.\n"
                    "When our design team came up with a beautiful design that included thumbnails of 5 different "
                    "sizes and specific cropping specs, instead of enhancing our home-made, simple "
                    "thumbnail-generator process we moved to Thumbor and now, we cannot live without it.\n"
                    "Thanks a lot!",
                "order": 1
            },
            {
                "sender_name": "Zach Smith",
                "email": "heynemann@gmail.com",
                "company_name": "yipit",
                "company_url": "http://yipit.com/",
                "company_logo": "/static/images/logos/testimonials-yipit.png",
                "approved": True,
                "summary":
                    '<a href="http://yipit.com">yipit</a> now uses thumbor behind the CloudFront '
                    '<a href="http://en.wikipedia.org/wiki/Content_delivery_network">CDN</a> at Amazon. '
                    'Their detailed experience with setting up thumbor can be seen at '
                    '<a href="http://tech.yipit.com/2013/01/03/how-yipit-scales-thumbnailing-with-thumbor-and-cloudfront/">'
                    'this blog post</a>.',
                "text":
                    "Thumbor allows Yipit to iterate quickly on new designs without having to worry "
                    "about introducing new image sizes.\n"
                    "On demand image generation was just too slow when integrated into our application servers, "
                    "but Thumbor makes it possible.\n"
                    "No more going through old images and creating new thumbnails before we can roll out a new design!\n"
                    "Our initial Thumbor installation took less than an hour to set up, and we haven't"
                    "had to spend much time thinking about it since then.\n"
                    "Zach Smith - CTO",
                "order": 2
            },
            {
                "sender_name": "Bernardo Heynemann",
                "email": "heynemann@gmail.com",
                "company_name": "viadeo",
                "company_url": "http://viadeo.com/",
                "company_logo": "/static/images/logos/testimonials-viadeo.png",
                "approved": True,
                "summary":
                    '<a href="http://viadeo.com">viadeo.com</a> replaced their Java legacy imaging application with thumbor. '
                    'It\'s been increasingly adopted as the de-facto standard as their imaging solution.',
                "text":
                    'The Viadeo Group owns and operates professional social networks around the world with a total '
                    'membership base of over 55 million professionals. Professionals use the networks to enhance '
                    'their career prospects, discover business opportunities and build relationships with new '
                    'contacts as well as to create effective online identities.\n'
                    'With headquarters based in Paris, the Group currently has over 450 staff with offices and teams '
                    'located in 10 countries.\n'
                    '<a href="http://viadeo.com">Viadeo</a> is using Thumbor more and more. We used to have some home-made '
                    'Java code to deliver images from http://www.viadeo.com. This code is still alive for some '
                    'parts of our site.\n'
                    'Since the end of summer 2013, Thumbor is a reality at Viadeo. First via IOS application '
                    'for member\'s profile photos, then our news platform uses it for new parts of the site, '
                    'taking more and more place and also some Android applications.\n'
                    'Thumbor helps us in migrating and decoupling applications from our storage backend. '
                    'We were able to move from NFS (centralized and very sensitive to high loads) to a distributed '
                    'storage like HBase, using a hbase storage plugin. Using the same technique of lazy loading '
                    '(via Storage cache in thumbor) we can imagine changing our image\'s storage at our convenience '
                    'should apache HBase start to show deficiencies. This is really comfortable for Ops.',
                "order": 4
            },
            {
                "sender_name": "Bernardo Heynemann",
                "email": "heynemann@gmail.com",
                "company_name": "oony",
                "company_url": "http://oony.com/",
                "company_logo": "/static/images/logos/testimonials-oony.png",
                "approved": True,
                "summary":
                    '<a href="http://oony.com">oony.com</a> is using thumbor to serve thumbnail '
                    'images behing Amazon\'s Cloudfront CDN.',
                "text":
                    "We've previously adapted the size of the thumbnails to what was required by our "
                    "design team, forcing us to have many different versions of the images we have on our site.\n"
                    "With Thumbor we don't have to worry about this anymore, and we can quickly iterate "
                    "and make changes to our layouts serving the optimal image format each time.\n"
                    "Thumbor is awesome!",
                "order": 3
            },
            {
                "sender_name": "Bernardo Heynemann",
                "email": "heynemann@gmail.com",
                "company_name": "threadless",
                "company_url": "http://threadless.com/",
                "company_logo": "/static/images/logos/testimonials-threadless.png",
                "approved": True,
                "summary":
                    '<a href="https://www.threadless.com/typetees">TypeTees</a> is a threadless app using thumbor to '
                    'bridge the gap between web and printing, thus allowing users to preview in real-time how their '
                    'shirt is going to look like.',
                "text":
                    '<a href="https://www.threadless.com/typetees">TypeTees</a> is an easy-to-use iPhone app '
                    'that lets you speak your mind by putting your super witty '
                    'slogan into an original tee and order it immediately.\n'
                    'We use Thumbor to generate mobile thumbnails directly from the same large images that '
                    'are sent to the t-shirt garment printer. It requires dealing with masks, feature trimming, '
                    'transparent images, and replacing backgrounds to give users an easy-to-see preview of the t-shirt.\n'
                    'Thumbor made this possible and simple without having to write an image processor from scrap.\n'
                    'TypeTees was developed by <a href="http://www.prolificinteractive.com">www.prolificinteractive.com</a>'
                    'and you can learn more about how thumbor helped them at their '
                    '<a href="http://prolificinteractive.com/blog/2014/05/29/threadless-typetees-neat-and-easy-'
                    'thumbnails-using-thumbor-and-php/">engineering blog post</a>.',
                "order": 5
            },

            {
                "sender_name": "Bernardo Heynemann",
                "email": "heynemann@gmail.com",
                "company_name": "globo.com",
                "company_url": "http://www.globo.com/",
                "company_logo": "/static/images/logos/testimonials-globo.png",
                "approved": True,
                "summary":
                    '<a href="http://www.globo.com">globo.com</a> uses thumbor to generate dynamic '
                    'images through all products across the portal. '
                    'More than 40 million people using around a billion images served per month.',
                "text":
                    "We created thumbor because of our very large collection of images.\nEvery time we introduced "
                    "a new image size, a colossal effort followed to re-generated our images. Thumbor solved this and "
                    "much more and it's a key strategic piece of our portal infrastructure now.\nAfterwards thumbor's filters "
                    "added depth to the tools available to designers and mobile web developers.\nThe extensible nature of "
                    "thumbor's infrastructure also helps it adapt quite transparently to every environment we need it to.",
                "order": 6
            },
        ]
    )


def downgrade():
    pass
