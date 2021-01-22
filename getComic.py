from lxml.html import etree
import requests

images = []


def download(name, page_n):
    global images
    images = []

    url = "http://www.177pic.pw/html/"+name
    title = "-".join(name.split("/"))
    print(title+" downloading...")

    for i in range(page_n):
        request = requests.get(url+"/"+str(i+1))

        if request.status_code != 200:
            print("failed status_code="+str(request.status_code))
        else:
            html = request.text
            # with open("text.html","w",encoding="utf-8") as f:
            #     f.write(html)
            print("{0}/{1}".format(i+1, page_n))
            parse(html)

    createHtml(title)
    print(title+" finished")


def parse(html_str):
    html = etree.HTML(html_str)
    pics = html.xpath("//div[@class='single-content']/p")
    for pic in pics:
        global images
        images.append(etree.tostring(pic).decode('utf-8'))


def createHtml(title):
    text1 = """<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <title>"""
    text2 = """</title>

</head>

<body>
    """
    text3 = """
    <script>
        window.lazyLoadOptions = {
            elements_selector: "img[data-lazy-src],.rocket-lazyload,iframe[data-lazy-src]",
            data_src: "lazy-src",
            data_srcset: "lazy-srcset",
            data_sizes: "lazy-sizes",
            class_loading: "lazyloading",
            class_loaded: "lazyloaded",
            threshold: 300,
            callback_loaded: function (element) {
                if (element.tagName === "IFRAME" && element.dataset.rocketLazyload == "fitvidscompatible") {
                    if (element.classList.contains("lazyloaded")) {
                        if (typeof window.jQuery != "undefined") {
                            if (jQuery.fn.fitVids) {
                                jQuery(element).parent().fitVids();
                            }
                        }
                    }
                }
            }
        };
        window.addEventListener('LazyLoad::Initialized', function (e) {
            var lazyLoadInstance = e.detail.instance;

            if (window.MutationObserver) {
                var observer = new MutationObserver(function (mutations) {
                    var image_count = 0;
                    var iframe_count = 0;
                    var rocketlazy_count = 0;

                    mutations.forEach(function (mutation) {
                        for (i = 0; i < mutation.addedNodes.length; i++) {
                            if (typeof mutation.addedNodes[i].getElementsByTagName !== 'function') {
                                return;
                            }

                            if (typeof mutation.addedNodes[i].getElementsByClassName !== 'function') {
                                return;
                            }

                            images = mutation.addedNodes[i].getElementsByTagName('img');
                            is_image = mutation.addedNodes[i].tagName == "IMG";
                            iframes = mutation.addedNodes[i].getElementsByTagName('iframe');
                            is_iframe = mutation.addedNodes[i].tagName == "IFRAME";
                            rocket_lazy = mutation.addedNodes[i].getElementsByClassName('rocket-lazyload');

                            image_count += images.length;
                            iframe_count += iframes.length;
                            rocketlazy_count += rocket_lazy.length;

                            if (is_image) {
                                image_count += 1;
                            }

                            if (is_iframe) {
                                iframe_count += 1;
                            }
                        }
                    });

                    if (image_count > 0 || iframe_count > 0 || rocketlazy_count > 0) {
                        lazyLoadInstance.update();
                    }
                });

                var b = document.getElementsByTagName("body")[0];
                var config = { childList: true, subtree: true };

                observer.observe(b, config);
            }
        }, false);
    </script>
    <script data-no-minify="1" async
        src="http://www.177pic.pw/wp-content/plugins/wp-rocket/assets/js/lazyload/11.0.6/lazyload.min.js"></script>
</body>

</html>"""

    global images
    # print(images)
    pics = "\n".join(images)
    htmlFile = open("./template/{0}".format(title), "w", encoding="utf-8")
    html = text1+title+text2+pics+text3
    htmlFile.write(html)
    htmlFile.close()


if __name__ == "__main__":
    comics = []
    with open("names.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            comics.append(line.replace("\n", ""))

    for comic in comics:

        name = comic.split(" ")[0]
        page_n = int(comic.split(" ")[1])
        download(name, page_n)
