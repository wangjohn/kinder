import kinder
import random
import requests

class ProductVariantsParamGen(kinder.ParamGenerator):
    potential_urls = [
        "http://www1.macys.com/shop/product/nike-dri-fit-shirt-swoosh-tennis-polo?ID=797196",
        "http://www1.macys.com/shop/product/puma-shirt-ferrari-shield-polo?ID=604407",
        "http://www1.macys.com/shop/product/greg-norman-for-tasso-elba-golf-shirt-short-sleeve-heathered-striped-performance-polo?ID=952548",
        "http://www1.macys.com/shop/product/perry-ellis-portfoilio-travel-kit?ID=717903",
        "http://www1.macys.com/shop/product/kenneth-cole-reaction-colombian-leather-single-gusset-messenger-bag?ID=276906",
        "http://www1.macys.com/shop/product/7-for-all-mankind-jeans-kimmie-straight-leg-la-verna-lake-wash?ID=1046946",
        "http://www1.macys.com/shop/product/levis-529-curvy-bootcut-jeans-right-on-blue-wash?ID=695171"
        ]

    def generate_params(self):
        retailer = "macys"
        product_url = random.sample(self.potential_urls, 1)[0]
        return {
            "retailer": retailer,
            "product_url": product_url
            }

class ProductVariantsTestJob(kinder.TestJob):
    zinc_url = "https://demotwo.zinc.io/v0/variant_options"

    def test_product_variants(self):
        requests.post(self.zinc_url, data=json.dumps(self.params))

test_jobs = {
    ProductVariantsTestJob: 1
    }

param_generators = {
    ProductVariantsTestJob:
        {ProductVariantsParamGen(): 1}
    }

results = kinder.MainGenerator(test_jobs, param_generators).run(50)
while True:
    print results
