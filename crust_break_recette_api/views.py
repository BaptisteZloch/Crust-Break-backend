import codecs
import re
import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .api import *
import base64
from base64 import decodestring
import os
from django.contrib.staticfiles.storage import staticfiles_storage

def detailRecette(request,recette_id):
    return JsonResponse(Api().getRecipeInformations(recette_id))

def generateListeCourses(request):
    if request.GET.get('recipe') is not None or request.GET.get('recipe') is not '' :
        return JsonResponse(Api().getIngredients(int(request.GET.get('recipe'))))
    else:
        return JsonResponse({'error':{'message':'missing the recipe id to search a recipe...'}})
    

def searchRecette(request):
    if request.GET.get('name') is not None or request.GET.get('name') is not '' :
        query_dict = {
            'name':request.GET.get('name'),#name of the food : burger, pizza...
            'cuisine':request.GET.get('cuisine') if request.GET.get('cuisine') is not None or request.GET.get('cuisine') is not '' else '',#name of the cuisine : american, african...
            'type':request.GET.get('type') if request.GET.get('type') is not None or request.GET.get('type') is not '' else '',#type of meal : main course, entry...
            'diet':request.GET.get('diet') if request.GET.get('diet') is not None or request.GET.get('diet') is not '' else '',#type of diet : paleo, primal, and vegetarian...
            'exclude':request.GET.get('exclude') if request.GET.get('exclude') is not None or request.GET.get('exclude') is not ''  else ''
        }
        return JsonResponse(Api().searchRecipe(query_dict))
    else:
        return JsonResponse({'error':{'message':'missing the query string to search a recipe...'}})


def generateRecipe(request):
    data = b"data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wgARCAHCAVIDASIAAhEBAxEB/8QAGwAAAgMBAQEAAAAAAAAAAAAAAAECAwQFBgf/xAAZAQEBAQEBAQAAAAAAAAAAAAAAAQMEAgX/2gAMAwEAAhADEAAAAdTT+b2S7HN375ycXp4mRlShbGyDCEwBiJNFSIuGZMVdl5EbZeOZ64moQ2IbVMAAjl8P1Hlefad2eWfrZbiulvKiVOK9+Opots68MprlZie2VYJb2c6PVDlLr85KuZdGsmDuYVyZvc+YSm3oWVUuZ6OL7e4ziS7QceXWZyX1WcqXUZyzqByvn31L5Zz7ScFhrdoz7pZFpGOcjTP20q7uznTZQDENDAshyO0EeF3fDr3uJViPZeey3GvOZT2vm+Z0j27x60biwGAAMTAEZPmn0P59y9FdhZjpPfm2+ajSRiIPXP2GnFu68Bo9RoBoLGJwOLI/BPunnrfM+Y+n02+a859PgeQ4P1HMeY819UqN3ocbnnY0DcQkkwcRWCjk+E9t4vl3jfXpy01aK7/KYxOc7DTz6Ho8zp9eAB6jEDAGJoJh56n06t8hv9Cjye30DOAvQM83m9P486Pe5PdG0IxANMcW5UCOB5H1HleTou1ZNuXvXKuUWEApUD349B1+J2+vFDXvyADAoBJIQY8XZR5g9RlXjV+mR5xehmcv5f8AXuLXD+g83pSDQDQNxYNENNL5PzXouBx9E+nm6GftzTiQiMg4aeOx3PP9/qxYnp5BAxFMUhPkSTqrDaajDYaTHoLng0FzzQNjrmMTAEMQMREiLXx/E6/J4+nfvy7M6NShDDn12w9Oj6Tzfo+vBiNPAIpgDaSeVu7kF4r68jBuhuTym3VauHJ2ZmCjq6zF1YyQEwABCWSCBoPFc/Vl4unqXU3eKmEqAjPCyHvzs9P5r0vVijh4tvHqDgQPRnAE75zaDpZ8limvJ1zi9HUk5J1mvFl2A871dwKUWjEDQiSBQRDEzwddi4uro2E/CJKICEpUCtPpvLep6ss9WtbZ5Y7UmOzSFdGtmGzTIxbWhiYmgkIJIQLP509Y/FetLjm8xfSPzzPQS896CATPBNWcXT0Z12eKTiIxhgsqnbf6by/p+nFQjVvnoeK5L3lZpeZGpVVGwzxNTytdBlsL1lmmgyxNmeVZbKpF0K5Krs8ydtF8DA8FZXbw9PSas8oqYVkxcM4urvTeZ9N1Y83n76Ns9uLoZUz9Hl9Q0ponFgCCQmo0JIAQIkJgmgaA5/R5S2dHkdeG1I8DbTo4ujozjPygrHECwMRJ+h6Xz/oOnKpi28NxlZCUSJiDPm3UnFfZiscfYoKK9tZTg66LfN+nzmqxNGJkRokgAGrcZR4G/Po4ujqSps8mKMMQtcoP1L+9we705ZoaFt4y22iZ5XlZlpxxfXSzRHJ1DNLHYt1lwZ52zTOtLKa9TMxoFyzvEyz0MouGEoyl8DryauLo6Mo2eUGiGRCKke5d1uV1OjJKrDt46Zyc9d85bOnh2o5mfuxMF2sjlUdwVuDRtZTY+dzF9KIRiajTQaYwYpRcvgdeLbxdHQlB+TjJSwJAIPfnT0+b0enKmtYNfOmfBhXpZYOMevPL7ZO4uB3xuDpuJEoTBVzxFlWTkL7KdDS11i2uuRMBJCBgS/P93P28XT0VVHxdEqpIxAlVD3Ovu5nT6scpGjTzps80j0kubyq9U+J2kbQNNQxOmCJVTrhZ8eZfQpiDiLKeW4vnnSaiuwacTwHQ5e7h6t7qn4siEoiSEIuv3OnuwXdeNcaT35o05VWgrwJ6YrKueeRfKiYywISixQnVFeLRRb103JAaISbUrvrIact5eRZ8+349nD065B4CZESYKNpp57WvF0ezDNxPRZvc4Me0jzcfTM872tug5S6NhyY9aRzTqRObLoBxOb6fMuLlemRCWskxw6AYLdLKrJKsstFEs2pR4Hfh6nF0WifipwlERhojF6+ep0+R0+vF4tS08cO3ri85dJp5n0UxfOX9xHH71LLiki8oKvKCLylF6oiaTKzQqIxpsxFux5rIuKnHhejj18HRNQIbjGWZUJeSr0dHp8jqdmEgx6+LpeVvj0j87CvTKDlZFjEhuISSikjm5V7kc3MO4hQIAjJywlJDtqkXOpx5fVB8HQKUIlFOArDVG96+ZdLHu68p0X8rXxY/NM9JLz3VOohEnFqxMTThKUUy5lmXp1y5h3lMEpQiREllFghOJOCjiFb4emUqyAiiwzkdRyW2Wnfg1deeW3m8fTz65eL2HrY+Pznts2fKdifkYL7J+f8AQIDQhxiinyE7fZqzzcenfk+qdWE4QyJEyLVpoBPzfOyz6OHocSMEQlCBZ14wntntuqu6srlXPTyZdPONFVOko0cjrrm0cjenRnVcAmKLCFOjyi+mqyc2O9dOMEZoqHCWbrcWEQlKmyPMaKtHFvXDQozGlS5jSFrS189HRRd2Yz5fUze/PO6OfdXOsImjbl1QgQrarAaBJoz15YL0VXzI7wRiZEhVXVLBEIuINWKPlwtWTXx6pohwlERIW6UXpOlbC7txTi/fklFw4yVEoyIxagsrmSIsSaATgGlUJxlQoxZBMrqurlhbROLIxI4OzFr49ZEIRcqBbSkXosNfHVsH2YwybV7mQ1hlegKeX2qzgT6sYhR0IGGVlhphoDPJkTdda3qucKEqpZSqZZRbXFcZqWic4eb5zfz93Jq4NSoCIEw7KZtn2GpduUYyViBU0w43K9fE810OojjPtURxd2mw816vPoEI82cBEURHVZTKxMTgQiEvNdNqjynR5vS5dlFrzQCEMO0Bvn2ZB2ZRiHqCAGAIBICcQhIIkgVAQkBBAKkJWwIIIUQ81zCXyXQDl0lWHkgJYgS//8QALxAAAQMCBAQFBQEAAwAAAAAAAwECBAARBRASExQgITAxMjM0QQYiIyRAFSU1UP/aAAgBAQABBQLJqXf/AODiLfx1ekWkXK+SUHzX/hdJAyn4nCbUWQKSMxntrEZk5osP/wBEpu1KbqBekzTkAn2aUrTVu1Mmii0Ka8zZE+aM0njmhgijTHywwYQ4SgJHjlMcQ5ROPeJCN0LSMdWh1bbq2n1svrZdWy6th1bLq2VpQLZaSr0lNSrZtE6226tp1bTq2XVsOrYrh64etitipxo8NoYs6VWK4fGj4VhTyph0j7vqHFxt/wAsjWQvqXExtIuAhQ2BCLiOFLAmxJsruE+0ebUpiZdckT7bVbsP1aIcLbfWP/8AT4Ct8IxNUb9SY0qNwn6oZriaFb9M4c5WfS2HyWS4kgIk+pe5OW0PJKRFpuVshdR9ty2TEpuFyW4dMwqLRHYKWRIk4QcaScJbDmzMKkjivwdonSMGRYmIYSB8U45IO3ii2w+kyYlN5I3UHbJ5F61AdGQJ7b8FWJEOrUkYerXxWu0tYf8A4JqrX07/ANR28YX9BaSmpTEpvJC9v294SkfhGGtVuFYYqFwzChqmD4ZX+Phqkbg+G0mGYVuOwjDUGzCcLdUYQowIsgUlvaxr2i0lMSmpZEytWmoHo9ufhrZCDwtw5UvDSshGiyiAfhJtcbD3CFFgKNX4drPGw5wmJhDmtXC/yBCIKdrHF/BTaZTaW9k8MsP9L+Mz9oKfUIqwrEmz3dvHfLemUyk5cNX8fbmF2IsOc01BxZqtbjIlaycR8pMR26/2B6UxkTnlkNkYZFEqj+kPN28eX76ZemNpEy6VfLDPDvSYwZCWqyU8THrpbSAGkZMEw6oUGND7mN+4ShUmVsrZYd5v/Bxr3SUJKTmw31OySaxgXS/vbJY5N8CsdKChpBWgCkkOrWzWskSUpRUphJQ5IXg1s1dvGPetvQk6WpL5rerVhnrdhKdCfs8OoGrEM5ugjqE0jXTxqWKaKUbHR3uEIe47hi7gBv33Mfw8UGk/bxVf3WUPwvWpautdclSsP9x2ZL1HHmEUQSSRsLHkMNRjuZKI5GMHNbsslI6Tv7gOKY1qTAqgiNKncxPrOElN8EztSV0rD1/a7MhiljvGYsU8YryBErCTYjzllj3gBiuGdkcjaiRXCE+MVa4MxY0MW0zuYh70NNROW1W6wvc1iEjSZ0pXyTNVQHKQSF3WR5JHskR2qkuYpELx355B3OjSTF3f5Z3vAeLeS9JS9KiqnEUYQytJHC9zY7ERYwlIyMxBECj3DY1lGjtK9kZrTtjjSK+M1xu0rkRM79dTdNXS+c33gKTJE5LVGS0n+WX1igR0gjyapLVXdxBqODJWyIxnGR2tVsG2rOZ7sFJypVqB66/yql0cELmoIaKjWo5UR1bY93YDt6W00Y2uzm+7BTcr5pkD16ezUu39yiXRpXWg10bbq0Orbdo0Lr236NLte2TTofWl+rbJt6X7m2XRofWglbZdGl+5oLo0E1aCUrC6dD9zQXb0k1Ma9HZzPdgTltSV8A9ejPPukn2YB+6NkhVmpJK4sYikF/KcxREhyOI5Jnu49JXTLrVlpEq1R/XowiuKWHrEEe3RRFeVsHbeBm2L+V4zrOiRyDdnN93HSkTLxytVso3rdmU9RxYN0qQc7ZopL3sA17xSHFY+CrqKj2TJPEEYWWlSibUc8s7Bj6s7cz3cfwTK+V8wevS+PO5qOaALA04LHUkcSI1LIQLCUESDTYZvqBNPDB2zDaVqRRXalk7cz3cdel6SuuVqTIHrUXdv+bV+xo/NuJxGj81fnr9nR+Xc/Z2/y6/2NK8RVz6ryNu5d1HSdFz6kU9apGm5dzVI27l3NRrK49tRdes+3qLrYpFdnM93G8LZLnavCo/r0vPMPw0UMhXoOZHI6JNDJfXEv49JkVV/ime6jeCV0yvWqrUtRvW7E0HExOFfsQ4GxIjR3gK2NHaRIxv9FICpG/ime7j+VMl5PiJ61G9JjypALJeIgjzFbBlLJSKQjjduSpEAMrnQwTSPf3JnuweXJc+uUb1Vp7WkG0Y2hbFjNrhwWCIYUGMbHdt7Uc1gWMpsQLXIvcl+8B5eldK1JWpK1JnF89SUvHkoqYSIb0WNIkKuGX2hPc2MQhCtlveN0N5FldiaqpEivvCC4l6Rav2piftgT7dKVopLVqStVXbWpFqGuRyMCwpEENhEc3Ui0MjSNQjVenbI5rGMcxzGHjvXkvV6Tmme8Av23yXrVq01arVBTpUtiljS2ufHlRjEPFiEGbDxqGLJiyT1h0d4CdovpMEVIYhF3OTwVMtSpSOvyTfeA8tIvItL4RfLeph1AOWXYDxbWPbIEpSG0ykmAtzW5XqrWMO10YM5hDci5rSUi5zveg8uVuUN0HrqT+VJDGHGYOqtpnGvZqkpDTRuNrW2tba3G1uNpHtq6W+1a8FvTqNcgdl6gHEc1OVEq1Ob0Skzne9B5elWztktQusfSlKNKxO4WHIRlAIhZkq4ZIHkWQzfdWxWwlbCVsVsupGrbbrS69n1NIQUUpZQ6jKQgByZCLZa60t660lJXwPyOSypnO96FPtROZUvUBfxZHUTRrwx3MSMkjTHfQBw3ptBeymOY93x0q1Wq1Wq1GCww+DBccYTK4UVtNaa01oStCVoqyUNLNc29aHJXWkvUtNWIMbZKWvmutJS3tAzmMc8IYxWveArixAPHBwoRAAFEkNCNLPNGkueAEmzAn4tKv271er0TotuVqa5fLer5QV+9c78t6vV6vV6vV6vV6vWqtVaq11rrXWutda6cWkOtIStVXpF6xuW9daRMoXqLner1f8Al+U8ckyvQOg6Va+Vy6VbKJ0flM18MWY7hllH1MkSHFDKKdnaxE6x4j5MhrgkcWKCa55OS1W5x9B3SltzxvMmRUYrHxo7l2Q0kcCNYALE7UkSHEsRFpoEazhk3O38N8uds7ouQaTLEWKQL3SAGMSYx8Z8lSYV7HtYm57Ij1MhQOcWCA8jcTupfK+V6utJXyGkrjI2sZWEz8czGCGmOa9vOUQzM4OMtbIq2WbncF1ZS5deT4F4NWoY5MdpIBtjEYcopZEMxHTRnYxwJdsOY8cKe0nFqGSJh+NeLC2mQnKrmvxaWRdTnsa6Y9zp4TmlPwkzz4fS9kHp8l66UlLQPJSL0yQ37JDohmnasTih7sUqHHxorCKwvMtWSrh1EaJVIIB6MAJmtRGtp3YSo/k611pcr10rVkDycihLxLozuK2E4QcIu9FGoo7o0l7IoXDNzyNl5UejYQQ7E3NydhFqP5OXpldaB6eWJSnRmriKaZhHjilmIKklscaMbcH2TmGBj5QWtcYaBacL38juxH8mSUud0yB6SZSADOiQhaTDQonxGueyIiSBC20zTmxIZSMMIukqq1sRhGk5FyXJF5I3kpecHpdtO6ua5Jn8xvDO9X5Ael317SZrnfKMqWWulK5K1Vqq9dK6VHT8OScTZFkWV0ilcZKVxbtcTXNeqLxxkNxRuIkK/cIcgnrORGhmbxnFGhEkAWt4VKUaVqbV0zXlXNaReoFXVdclpM/mg+l85JyXS7xjevDgUjYsdqEEMqGjCKiwgXbGGwqVZK0MpWMWnDGtbIrsa0baXkSnZql0b4g9TNKv1y+Renzx7piM/dbMhtepyt234MqqECuQpWyNwp/+Niyzvlcq5Lyr4Np1Npejgr+XJeRMh+n2FyWkRG1tCs8AXIrGKxoRI7nXwzWkr5Wm0qXoafmq1W5E8FofkzXlXJe0vIvImXymTfXr4Xk//8QAHBEAAgIDAQEAAAAAAAAAAAAAMUABAgARIAMQ/9oACAEDAQE/AcsjQcyj5LeQ5lHzHMlGg5sUajm5RqOblGBzcoxz6Fb0Rjn0K11rrWWslr7rLFaxRjmSjHNitcq7yxWsVrFLebzfyxWlPWa+StK0q//EAB8RAAAGAwEBAQAAAAAAAAAAAAECAyAxQAARMhAwIf/aAAgBAgEBPwHEw/PnpygfrQB2s17rzTNYswKS0+D6Dg+avTSxRV6wWEiifrBYnzRPLUuaJpalzRGWoxRFqMURajFEWpRRFqUURalFEWpxRFqfNEzSRRM0keazX2M1PmiLUuaA4LUuaAuT5oC5PmsSKItJFAcFpYoDgtLFAcFpaA4LP//EAD8QAAIABAIHBAgGAQMEAwAAAAECAAMREiExBBMiMEFRcRAgMmEUI0JScoGRoTNAYrHB0VAk4fA0Q4KSY6Px/9oACAEBAAY/AuwD/BK3I97Ptr+S2p0sf+UfjV6CL5RqK0yjY0abM6R/07SFr46wmkzRcnC40+dN248vywvxryMXStEnMOBwAgSfRgrt4caxrZs2YFAqwl0FIdX9ILpmHeA50UMeAgz/AEOVLlLxzgPo8mWsvhec/kIGiPIsa2ta1+kWsgYciIyjIx4THhjwxlGXdzG5A72cZxn21mYsfCgzMXz39Gl8EXOJ7SZYDYYnE5xJA0GY4t8QYYxol8gy/I8c40jAeCAxFJc7+f8AeNOmcJEjV/M5wZZ9suI1TSr5VeK4QjFTLnoCFBOdd6x5KdyN0bPFTCDP0h9dPPtEeHp2aR0/mNH8lp940GppgP3MaTXDYjR9Ll+wc+sT5s38ScpmN1MTmU0Ivy6wsxTXDaHnGjaldql8wDhvZx/Qe5h3V6bwnlFJ+vw92CZJ0j/yi9jpVc6wEdtKogwxiboo17I2Yz+kKk30i1RTZh0l+lUmLRo9T6TIP/x4VhjKWbc2bkVMCdKraee8m9NynTeN0PZoGtG0J7ccss4fleco0fVsgfXHX1p4ImautlxtrygSbhLqzVeow2eIg0JpEzbW8TAq5Vt7JXVv33jeZG5TpvGlXbS5wMGqTTxxWn/2Qt6vt5UJMUxNDT8SClHuAqduBsk1y241dSWrTx8YZiDRcW24qCxA/X84WTKwQZVMM0lrgrWndj49yu8dlYLNZ7q/LKHmicCCQQD94YSTrJnDCnL+okWzVlzBLCTKxes+WDiBsZg8T5xOlmaNuXYGAx6mA7tLvDA7K0Aic5KUdiy7ONSKRpSmbXX4Vpwi1J4tbxXCsI6zzg+Ib3a4QRKlqgY1NOe7l/F3dnufP8o8w+ypMD/TP/7RMCyilnM7yUOu5brvHmcQNnDjChkINlWPI8RDaxDfU2LlUcIBaUwNOcSwBajTLaHlhjBebNlsSzLqRgUp5wrNIdQ3hJYdYpLkTG2bsxlGkTFBC2MMekMhaX61cNrEUxjSei7yUPI7l+u/AnSw1pqOzIfSFLKDaaiDgMY9HC0l2208o/BP/uYb0dCt2eNd4g/RuW/wQ+Eblum6lzWU2uK9MaQ6ypTTShINCBln+8AgNQzNXBfXS7RmbolytYtXFRtQZr5ClfrEwF1WyZq8TmYsvW7lXGFo6MC1pIbLCF9am34drOH9YmwKttZQs7WIEbm32i29anhXeH4R384zg/DupQCTDWt4LVHiEOmpmzRdsOniraMYLtfrTOr4tnw50gP6NOS0INkC6oriBxjRXeQcmVrVGzXKsNLC3VIw+cTZKJOdDdQrS4m0Q1JVJjTq140tpGj/AOjKWFLiy8gYIKTgrYAIq++eeUMupcLR/GooOh4xo3qp6hEKMFlgmtBwP7wWaXlKlqC2eFd4/wAu9n2/LdTJi5qtYvA4jhWGQh9k0LUwrnSNkOMA20tKg8YlSQgN+OcM5yUVMSzNRtYwNVQXZZwUseywPfbhE0ybpbqtwvSJd91WVSxC4LXnBPrAMaVTxU5QSAwoaEMKEb2b13IG6mSxmykQ8ubqwx92tIcAy9U76z9VaQrEjCSE+kXKUphnngf5h5QNLhSGYPVNqlxqcaf1CrVLTIEpjxHSJqlJKFkt2K49axYpl2uiI5PCnKLJpQUDWrTm3GGqktLmrRK/zvZvxbleyVLWcJdrKz451NKQ9mkC1wFVQ2W3QnrExRNm3JM1aEOa8PrDzhMY+seXQ5UAwjSpaT5lUlh1Y4nz/aK3ThilgHgpxrE6k2ayKAtGauOcTCk111ci8AZVrxh5YRWopYUJ4cInPK8KEY3UJyrFqKAizkVmux/LTfi3KdeyjqDiD9IuKCttMMPOFG01r31JxJguamvs12a84mS7nbWC0ljjSFud7VpsVwh6e21xi4s42bSAcxAmiZMwJISuzjnB0cVsMazWTBVgxUHAkbupIHz7lOMVuFOdew4jDuTfi7+fZLw4/lpw/Qf2irWE1W1ZnhbMgfQxoiS2mKlBshK02ufyiZV1IwoBmOsKSKlZiEfWJkxfxdfMFeNLTEqSFXUmyq+yTa0aA1MRNYL02o0dx42RzMPPHj3JvxblOv5ahi1pSkYYU5QCEUFcBhlDMFALeI84oRWNbYt9KXUxgy9UlhxK0hdkbOXlDMqKGbMgZ9yb8R3KdewbbrT3TDHWzceFcBFuvnD9VcYDax+nCCNfNx44VEL66Zs9NrrDeumY9NmAvpE3DjhjBbWNT3cKRb6RMrXxUEBta1B7NBjDD0iZjkaDZhfXvhngNqGOuahyFBhAX0l6+9aIu1zW+7QQV9JevvWjCF9e2GeyNqG9e2OWyNmAPSWqMzYMYJ1pt920RT0hq18VghTrjQZi0Yw3rzjlsjZgD0ggjM2DGC2tNPdtGEW+kNdXxWCFOvNBmLRtQS00uDkKDDuTfiO5Tr2auTZUJdtDPHKMGlXhmuFcqRrMLSdnpDSTMRQGoFsNThzh0RVALKstj88ftAYihxB+X5YerXV3KtScTXlBYGXTkGqR17k34juU69l8qaEqtrVFfpAS4eJjWnOGA8JaqjlGMxdTddSm1F8hyCttgdiRhAUmpzJ8/wAss22W8tRs1alDxMJeJYWWhRSvtY9yb8R3K9d1Ndc1QkQ8tg4cUJumX5w0pa2GZLx93Kv8RpDq91ja0AH2a+H7RKd2Ia6+nXhGlUmt+EpUe7jwiarawWvQCY1WGHOJbXzSHemewBTKkALLmCkzGyZaSvOsaOqTbKFS9zbWdKRMmchAsOsOpdaj3waVhT5DeTfiPcy7q9d0VYVBFDBtLknMs1TD1rtkE48ooB/29X8oCjhhD3V21tMHaZixqWY1JjW3PndbXZrzigmTF276hsawiWDZoQeMWtlUGJhFReCCOsAct5N+I9mXfXr2DVsgHG4Q21Kt9nA1jxSb68jSM5dnQ1g1Mi7hgaQv4f6s/tD/AIX6c/vApqLuOdIP4dnDOsZSL68zSBhLt451hsJN3s4mFosn9WJ+0NsyqezifvA2JN/HaNI8KWc7sYPq5V9cBeaftCbEuntbeXSGrLl/p28/tC+ql19rby+0EWLZwN0V1KX1y1n+0KNWtvE35Q3qlrw284WklanxesyhhqhbwN+cV1C3V8Os/mFGqFpzN+UNfLtHA3Vr3JvxHcpuZk8rdYK0hmcSgoFarNui1Jm1S6lDlDol9VYrivZ6LqPZuuv4RQT18Vvz5fk5vxGM+5l3F3MyRdbeKViZKaaoDpbWXKtMS5161RClFS2vnE0ibVJjlytuNesaxZEsPndSPS9cnhsts9msLJ12Wka6tPOtPyc34z3s+0djberw8XKGmOTdaxFwx8qxo6au7WUuPKsSNiTV5pU7XDGHJlWAHDziakxq0xAphTyO8cyRdMpsjzgzACzgHClNoQgqjLdRjbSuNPlvZvxnc/LsMtxcrZiNUFGrpSkJSUux4ccopqxS+/584IlpbXGGZFUFvFTeFTkYW27ZB9rnCNRqpjUtn1572b8Z3J6dkwUJ2DDDiJIGXlEpxdRFmOoszxw6RJDznNXpgueXlDAzHciY1buGMeoYK1zFrZeORONY0yVMN1qZcjWNIZXtwShpljF172TMwV/QMdzNK52wJYmqJjB7DXlxHlGjsGwM21QJtcK4/EN7N+I9vi7mcZw3YZkw0UcYaY1aKKmggNlUV2sDHiGPnFyMGEFbsVpXeF3NFGZgOpBWmcIEmISwqlN7N+M97PtbseWM2FImy1zZSBExkRMVwYnHw0pEmspCq1rVq0xMLLKKhHLj5xcyrUtwbkM4mswUX8j5ndtRLzTw1zg6Pq2q6PtE5Vyr5xLmamajl6nawC1yPdx+W4m/Gd2HCBhXGppBmWlgDjExZqOmqUFjTCFlbYdhUVWkCT6sC24lnoflGbZ08B/5x3hYIXPBRxgz6EAA1HSJcoJQuD7Y/wCHezfi3dusZV9oDiI1bEha1MPWaaOFrhy4x6Tfjy+VM41usWltpWgNYQGdlMuJFcsMM/KMxGYjMRnGcZ95lR7GIoG5QJJdAmrKG1YQXy6B72onHy5DcV7s34tyOzKAVNuy31phE6kkOUdQATwIzwgyNSAltQ4OeX9xMatyr7HDw1hQ0q1GoCPMk/1Gj0Vdt2V7jy6dmXbh3Zkxa1A4CsVuu9XUjV0t4V/2jFqNUrWnI0iTewKu1AbPFtU+XPezfi7ucZ9pHn23TigQe9lDyjqpjYFlzi1RLE4DgMaRr6S2qvj8oSdJSUaeFl4QuwpWt69efYyoysVzA4RUwMRjl3jLmCqnMQTRsVtO0YS0HZFBjEoUakrwiuG6wP1jKMomj9e4zhh2iwBmVgwBOdOESw0sWpJsJv8AFh/zGFMtdVclHa+vDKkGQ9tdoCmVOEFZooSeLXHIDOFlisvaAwauHtH5xN2LatWt1a4faJ1qUBY0IbFgWBiyaTbqsTf7RFKfaNHd1JCKMbsF2aH7/kB3prfqO5bp+cyjwxl3Gbmx7+fYen+CG5PTtfVsFbhjSCstsbcGOeVYDeqtWXMLDmVMShWUBc4fPGgrCMw1ZE9Rh7QI3bTQQCKZisU9UblFuBwrQYwsxbQ7LxyiUjqgv8888R9N6vTu59w9pEy2w53ZRjJlmoty4Qvqk2fDhlCqJSAKaqKZGKJKRRW7Acd3q2ZgD7ppEz1071lOORGRixXcLq7Kfz1iQbtmSMBT8se1VVVNZi+IVEOgnNZKlUFcsAKfWDtTK6rKmFbaxJrOmFagdak+UJtu543cDuyZd9blGycc4YLPmUNqMcNkk8ISYzlSUqWEaMJrEiYPczwJ/re1w3J7LNaK3W5YV5Vh7GrY1rde8NbMVLsBXjFyMGHMbi2bLDryIh/Uj1ni84OxmlnyhXoaoKLjgN6NyewydSrAzme+/ChP7xPYSvXtpVym72axpTpLe4sNUVplGmuUZjqwJO1xpCXJMnHUBbNrZbnhxjRQ0uYyro9GGe39YlJMLlwMbs40KYsp3WW5LWjyhZglzAG0zWsq5hI0pkSet09bRxs4xPMwzLDS0MCP370655FLlo2sYY8h/Uaa5mMNJScBIF2NPIfWFVnUM2QJzifLae8pZej3pa9uP8xocuZNeUJmjmYxTZJaJc2YasaivPHdjcnr3TIsIwqDzjUhGZ7LsIOkWsFAJpxwhZdGqWtjWBHQfqjFZi40oVx69Iaz2TQ9/IQWrLqmZw2YDuqbOTHhA1iS5nKorAE6UjgZVGUBVAAGQG7+Z7cu3LtPXuvODS62lZeH7wdISYbjLK04Vj0fhq7PtEqY8zEEM9DgTWphZbZj+42lTWMTft840hmoQ71B47icxTBHAZbMxz88YsmLcySAzKwrwjRZYKE2Y8wLT9q709TuM4+fahFNqufSH1cpnZGVcxxNIaZLpcPeiYplu7y1JNowJGcCRayzWS4Bh5RJJG1MS7DLdXzDQdKw5L11Zo1BWka4v6ulawFWYpYrd8t7895SZXCsTAGmC81zyxrhBlkmhicxmP60EU5V/wDyBPM1mYCmIGOFIlqJjWottOfnupeqD1EwE2NTCNMsH4toFOlDDosmYVUClv8AHSJEuZKcauXW6mBbz+W9PXvZ9o/wTddyP8E3XveLtXtWuprXazyjFZVbveOUNSVLOOzt8IekpTTw7ecN6itBht5nlABlECla3D6RpDa8qUl7K18jAlsiGlbrQef2iQr2etBpQ4cM/OJUtJhl3E49BE6nrNsBQTSmzWHbV4CmbUz/AIiSqJRWG0T0rSAhcBmyHOFpOl7RouOZj8WXnTxcYNZiC3PayjxL9YzH13rjz3K7ilcYqyITSmIgTNUlwyNIoslRxga1LqGsG9TtG40NOFIJo4rybLpCzQXqop4vlXsyEeBfpBqimueGcGstDUUOGcV1SZW5cItRQq8hvH67kbiePex8OWVMYmupa2lAPO2JA8CKGNpNaWtQD7xowVnprG454Ew9TXEHOvD94nrLmqRskFnrmTWJssTNpmvX1tNmuXlGvWoqgpxIrEmXWss0BJz9r+vyTddyOm7EYADpBGrShNxw4w10pDd4sM4sKi3lFwQA1r8/+H8kR597PtHT/BN1Pf8A/8QAKRABAAIBAwMEAgMBAQEAAAAAAQARITFBURBhcSCBkaGxwTDR8PHhQP/aAAgBAQABPyG+/TvAyiVDpUSV1qB6T1DHTHoOtei7tT5jDLpnBxYy/OGMRQ+3CL6DB6J676XmKBbg7z7uRNn+cxw87LpmAtgdgfbLVijqJ2mKjKHxwmHrXr5dyPboVw8QajXWY4ldBLJd56HlLSnoM26VKehpNYHsKz2l5Y1LHvCPp1qwY/C+t+55asH4jwO5Vb5faZckzpY1xUaL3NRHNGIi/CeEm0WRNHIMQU1fHRRMF3Q5HUrtzwTxTxxKNiX01ndce6J0VllTzIsy6ENU0Icc7MOOHYhyEu6iE8IrzAcwirzzFG+7evneUdcu0N4Ev0NyOa4lip4LRpug6Sd/uStAzxtfpMU2orZh91VK9qvK0uInHhY+x2mipAQ1fiVK6V/BRGcuPqbFS5voszaVMXMxx9SoJcnaV6KlerSw2Z6XN+A/QdHg4/hAqN2LyKOegH3gwOmPvZFTFBjwBH5JaRtl3Qr6jMLYVkaQt7QcW6yAxHAlLz29L/C4N9pmKtoylTymO8FExHa7P5Ad0CsKWUUUr9yoSuKz+p5dEx8xf+ustcxoquxtj6Q+VRAQP/cRlLQ15/eI5tiWqlO1wn7es97jqJkKU4a/k8xB9kQJS4BEawwvafExLKjtdv8AEdBZc/ilKa94Q2WCEreQ4i1e17LYZNKDyw1vapVEVDqzxEDafyB6nFTWQVgiBABiZRk5qGO/Tg/jqDh/cFEAQ/ExaVKdpTzAYRWXH8Q6GJOC5Rna9Ll4Hoe5mr8odmGG1hgfxG3eZFMq4PEyGdnC6/Uyh5BuGGQKugFo/MSVOw0Adoc1AM45KHwxpDmnXMtohg3PTfqWPkfh6B2i8X0Ay/8AXLcQ7pojv+f4TrppkLkwt+YU49nFOqDMxUAvlxb5lKW0FKsbE3EiEEZWNi/c6xRLNk1rZu5lLwHTC2HFk7C+IDk9qx5hk3gCxZu++YmZsBaO480BHHHMxRFh7BUf8kjqt/46C5f4msO0PRmfCaF0O826Z+K/hPVv6SBWMnNFxFDMC44+pQN44W7v+v5H7pfjoyZTmcmpfEzLi0SwP9x/JWe0GVvBjeeFxGJdGppcOwtUNvv11+oxlBpPh8eNUiZA6A3yIyJQEXm67HvZUp0TZbx8MRkXG6BBrZtNAvN1TL7xEWMNzbS/04lVD/S/ye8r7hrMhQzEL0qKup4PzFRt2mBPD1vqo4M6xBRQa0xA0PDZgOD4i7a74RJJp+jVfuLcJTjWakqrd0wduDDwvN2rTX+TPhftBmC3M0y5a7uUypMR4ex/NfoP/gVlx+7p0IamOJXmZ7x02jiIcn+P8JnEDHyFmx+0OmHuMJbPsqYxplxmruBCj0JoYnbfjaYr5vENRv8AkB+4zU6DCkcfMx83pXo7S61nLWZz8QVUey+PMz6+gpflxKL0KQw19ogEGkhb/Ir7EQmaiGjEycEbuY7y40Rq6ph3/wBvSdB7dHk8wyBBcos0cGL0iJ3tVj3HRbucQjHg0djXeLKUqBAW0gzWZdZBmoCw20zWjNYAvIrf1F/vRJYCrst3E6iSityuGpGQovgbg795RkVLBSZe6OJpfu3UXG+HvpHuYpto4KaYBowGHBYvmPofUS7tA+pr6BQ1lmBZZ0qeZpTY5c2/gIWAsF6TLkhrgBS1lMfQMdNTmommNnYIdoLpCnVQ5rxq3MJKPAEqFo4UyFeDNq3m+KI+comUo06jUKQdlLYK2LlcBCSBZT3Nxyfm+O5DX0sfTcer0B9EsSGuhnWVLcsWM3HYOYVIdH8R/hcYBq6ZJg68FqlnPiA7WS3TBXFaRYITrlaw6HTTaWNFbBpiasI9rz9RULGYw9bvmHrG6TYDkb6ykDOp6EtfgQotCRvn5e8r9TSDdmd8G3MQq6X0abupm/8AJnEMypQyo6YlXtcqUI3tmYeX9RjZ4mETS8NV8TA8jVgHYK32gRNXrJpfZf1EjWRXc2rmy77xiArVNii3/i5easZbKjivO/aCmAU98n4qKV7MyC0by1LXuZUVYq87XBLcCaDKmO9RHfLoZ04yQ6nU9d+peivz4IHiV9SztLCVlDFYijCINJuLArNqyKxErg3FvNmsTymp3JeZQzWV6gppzUXAsrcFBfARYTgatNFN46r2t/L/AMld84eLrplPI0CnaqU5yTXOW4yoQ02p0vb0npUMriJBxqtINl7dGU1jC6vMyMXrRR7yzFpnTvBAEdQOno+7lp5w5ucENM1KOCEIqEo2Y4YwehDWPoH0vo26FELWZKplJeFjHA+09x7tinZ+MaId7E5/aeOQJaxMeoTtVHjSFygKu4O7RFTdYvT9VBDVCnGqr+Xo+96C66TMqneeGfPzDXaUn1fQ9L/g29W3oBAESkjp3yWGFHxAsgKaBgr5Y+IhAzQouHUhY08kyMrZsIa9zYV5n6y8KxNpokPl1IoVd3MXee0tLb0meZbnPQ8mmOkZhxlI+YvalPwmMRpvBuh9mk2hhvLfUyWui/sMTI++L/A/E8W0fox+ZbQFZOflibsxWw76XK8zktbXGlTT2WcDyxcMynmfhj8xrrzX3sfiGl1rCd5j8x0wVXLTjSpi6RTjLzesNSFKy/ZVTPtZX7WMe0A/018+8wsmf0vab5hjQY51gTvZtTXFaR0Ph+07e0KS26/+j7xQlH9K2m4PdYHu1mdugya4rSOJIn+5XtNdTCR8Op01igIYgSu0qf5iZKy90Y0G2MU8NMs2t2NNZk3E64rFlxcCya73w++ssuAGgnGn/kvSxKiOTOMqgMrRGlpGvj0MOp6X+BmuLsG91h27wTxFWV/D0OUsRlZi7Ir3n1ncOh4QQsvG8sqru8sOsMUktNd5mYuVd+p4u4WK4ZZgaXda+8DSIA2WHOmfaPnWaFWm389GHpOh1dIdDo9DpidMVTbVZawS7gaLbBtxjTvD0KKphuppwTRMczy+4eMTt9wa+rG03jCOSENOv27wVEO565TW9tHE0Tj3wNH3v7S1HANiwfh9peFh9lq8QT4jo/a2Siu55d5X25klHO7tB/ebHKe9jWC3MgGia4M1iIFjTaw5vO6vackY/Oh+ZfdZWKwX1YlTNtft6GHoOhKwkZRAQaNJq4RcSvP1AlEyi29EdBl56XfGDkgmIts1YC3aLUe5bR+JaaGy/wC33gaYAPaLIWCp2Gyu9sDzLGh3Yf1DbWHMW0dhjl+u0zlBoA2G9fM1D43mm/iDAo8oA1UbQDdAB0v+EilFJxlfM7CZ3luijiY1w6QLjJVXxTA44aYjteZWPlnT/NzR2eTU/icuOnC77yrZ1rb/AI959H/T+o9ydel2ntLye+01PwT/ADcvjnO8naX222b5xF/WN8M+84EjvnjRj2jeDWaYh5qGFp9zPxUsT3wh53TAZoXta3pWfqUqhNq+WyZDJ0XrwdU21jlr4rEewJt1zcb44b5eKzDIENP/AJYhnVoMPxzNiMd97axPpaarnCNMYDH88VmGAlpH4NupKShi3AY1ldoacQ06Du2W7pl5JePS26k2HGtXLyjwq+QI/u22Eo1SzMEEZIF1v28OZfcl262Ws6uq17Q+ivL2+7ptB/nIM0hfS6N4vBC8eEO6Aqpj1Fh1dOl/8e3WYJgsALvYwbCohy1lnXEE+qmJeX6he4mjO4BWj7M1vXvBB8q/4Zm/W5cvq+g6vVQPJOGZvrHxK8TE5ZTlB8TGJFDl035xkEtgUzg5qpph2cmkXpyxUWy80+HaNwCHbhnkONsTKZKQ1UENdKRyIx9BHo9BzGU7R4ruDjvqubMUXuQaAZ5lqo4Q0/gPQqkadwxL4hwSgytyyao8bTHDZS1Q5YKTclMSzLZTrEmW1uzqvGZ95lkMIqwLE1Pa3PTbqeipSQZc3RTTT8xfBoGWdSvL3hLV0IVLd+bnoEvMuXn0Ho5n/SVD/cPD5inj5jykKuZ2fqC7ZjcLZDAbsDRq4lCdAZbNokSPJDgDuNoPufh+50GeJQOKp5MacZiYt6VYgN5vcmHBGoJparOnO8u4/eYOc/NYhuxoMZE931H0jBzEj9IVSTVhDCUkyZpiOJLVFBmOxfjpRGLlwYdCEem9/wDaDTLFMNxGj9IRx8QBlOZisEoYBLFdiMrM22OevAa8Q+LhTQc0wqU2znArTojc4Boe+SUtSu9S5vH1XFg6S2mgRe9sDSostQDUMNdblykIWfUoAg8SsE3b8ylswGHJHLTGhpUWbzM9yMpn3DzNxmLvHKCgnwde/EtQCwqlNK1yZK3jt7RuJlwjdWRQyqAyNHONZhPB1LbM/JCb9Now9N7W0go+6VEEabdNHur1g7FyVxliOV216o9MthWkbuljWEerLRLUWGuIBtiWOSCL3lnMtyERsJi03ejH0jSvHKwlyIBrn/2ooaWdbOw7/uaeUD7L+cTwuOC3RvpKF7dk2z4wz3lbPQ6EqWJowldD9AvUdkYrp1HVfnSWMgW0lNY/pNpXRg59HX0r6LH3ywMQM6THHRVdEx+ZjxKhCxYjcSAFP2C1tu0vRFA34+8+0SmoARrXV34g158R+xXaaBEXVGd9TWUA3T2Wh2sNbl7B/wDan/ahRkQ4ERt+YNmkHcIlpV+IDeMG7xBZ96F+UHXAteuBM4qaN61LlYZ+xBIx6eehoiYOqMJoca5oQwmRoypTU855hK37QDe7HgIzZ8RF+w3X/bdyh4ChFzQv2zENeFCIEkMwhAOhZ3vXUgarCKIUIJo8pQz+rAy0p2nZHdjzx4sTdDMMkJqwncYnGeO64hBTa8ysBd1fhOLS+5LV7aTY5W1GgxhVHdhyOgnJiY2WLqZi+uyZ2m75zFxAmkvaJGeUqNGa7Sxi5QCuk3j7j4rBLtfz9xXlxMH+mkbNcg0GzrniGTDgeX7g5DrgYtmkSLBKmWrvEBYA1WX+YtfE1Ry6ays5LLEv4gFqqBYQKN9e8wK35rhbb5e8oCG99Glm9dFJSWdKkSGXR36AZ9eUrEwfqcplQco1JKb2lit7lpqmd5caKWLQEWLjZixZgzPpm3bS6PoMbHFbNnsqMVYY2FzuJjPaW99E1Yv7RYRDWiMv2fEq27+Ni+DRXeIq4qLYs18KmkMgTADxTrEDKJkKH4Mr7zI4Dyka5aZi6Lgy+tTt6T2wSzJ7TAx1xN4Gzfug1xiLZzLeI5Yaa9BlwMsN4SONEWZcvouXLl/wgHn6K9LX6LUYCBZSUP7y3hC3UA1zT7m+tR717TWYu5bSVGLgzy5jrPf/ALi6knQvEGXL6PS4MuMet9Lly5vLjJSoYilyxbPe7fuOhdRHEsKUEfBPmV2fMMYlOmsze0X0Y0EiebS9l0uEQLo3Hea9iBJuj6Bh7xsDVJQDh8x/lT3C0yMvq9HrtLiagAqC2romIHXQLoHsVca4mTRGDR/qJYiaK7Yg7Vl5JtKjKhAT0EGLhjAVUZpZxCYHLUVrEMyVeJpiL4ZrOhboKFLfMSL1pr7PE0uhTDg61KndpjyELkFRR5eY6Qh6DXqxa7hWxjMWbrDZcCnGpUJHNF8EnKWDXy1V3r7dU9L1GLn4mALNOmcFE+Ii9C5XmZ5hkXKGa8NiGqjEuOGmrucQVKgBE2WlZWczP+LUwNcNnHtERxjWgy1QtAZmAJKl+bNI+p6sWAOwRRBhY8YzBhhXdVr5JWReRZy5xDhBZ0XyHZKw7s0db6Xn1Lh8Q21Ki3YjfQrccczswaZiVbWLPbFYRWreFvxl9pViuVbDUmU0ahfeFjdjby9DXcMrVB6votk1j36MOjM4mvKLmRcaq3/mhOICyDjtit8oF+DTS+8voxh0PRfRezhiaJmdlTOcdDXiKatJrfEqSOpuGDMaawxNgbIryZxi4pGwqmjdbHXSNZHOjmhetxypQogjN9zvNOisa23AZ7z5uQVvlmsNnyaSJJBk2G4fiC3H0swaAdPEuqCqw1mrrxLh6C9ie4BavN+dEAP7qNGuUY08CQPgbzcT2xnb9IlUbMhWv3UHE5KbEX01wl9dulQisOF/MpY+ZfMPFTDmXPCtYF1qpwei6kYw1jyxSq1eNd4Vd0SuyYzux0sKq3P6hrh2jAnPlwQWgKAS8Y2jnvdqtfij1nKQcxh0OjQ2GzGkWc+Oy3k7RTxzKfFdJpF81vhGWLYu9kGC1AoDpqOly4MvpfRqF6fmgBonYEtBLeZ4JfipfMUhBpl9Oayjea17hX3KqS5OqAIe03StQeyDKp4xa4ONKlSjbdeT+4TRBvIQgp4Aomj0KFvjjow6bx6WCVreo28akfE3JuJfg5JgqFJdaztdfM2jCWE2m8uDLxLlzNFir/tPmD5llRzjTp4Qw65imd0dtg6ajoVGlXPuoy3CBk1GuMjhgaEhAWZQrHmWkCFBggz3IYtEAGqmWbmgGnOerN4aQ16svDVrC/CJtAW1iXt2gYRR43SUFkA3jboR6N4wZcuMuprHf+Y9MHMo3rcvl8dNShzKKh+70ENggAp5gKONzXKNHMwEhbvhH9SpISxqoFPhLHFWqa2DjbSNrkqFaaXf++rNUIdHToDppJfLWMBbt9SUT8y1gPraae/VCL6DVFmXJ9nowYvoblnViwVvmCImOZUDuyuyYuUbwVRyyodN5fpdemqD0PWx6PEvBHoYpcuLhF5L/mO2cy+ITU1LS+7Nc3U21n58Jv1Op0dYw6noHXboxcRYro9Y9G5NQb5Srl0vrDNf+JhsRA7aTyVSozefY/V3nxTqO/TWbUVchfJxhm3GbfvxiHoAFYf6HmObu65T2fuAwfqqKo430G9qhbUw6GEXfhvrKhtAJqudlFO8ZaAprk325h+L43LX5rTEcgBrrsKflr2jqqyg1xD+5kXU7mCko0r4DvNVxFrTHDzNT81g93E19otx0g+9i4sSxHxDoWDmDNelJTWssMaAcRzuTMtWZbaZ4iZnCpvpBXi6GbdG/QmxsLq8x4t5QWuIoKMuqL1lGOOg3sfyEFAFC4c4Ciqzg7YjBJrVulHw0JjJwGwtZO9dDg2NMaRyaC2468wcHZ3L7py8IOHDMLIKmvs8QabaBR1PS4uk6DDHKcrf+Z3h5jfmWHSPBKeiec+nHo+hjbl2UuRAdwc47R6SiP8AejKQqDcWrH+YmHUsOTK/UXAx1LUVu/l3l/jvRfgHFUcESuBoKhq9zxKtWC2wF93MtlqmpVuO9H26MIx6LmmPVamV4s10KzoGwa2lriCpiJuFzWU8xMutenPTaPqGsBfY4hVEXeFZmM1EK5td+YGmsbaneWMMdGMaQcOZzyz9vmbxm0uMY9BfQeEmkq2aOkqNy/MqnmarJaN3rK7yug19GeuiHUmiHU6x06EdY9dHo1Tbo6dDCNbCf53MNYdBm3T/2gAMAwEAAgADAAAAEJfO8kayrgGvBAsy+JP9mzfBqW5Rmk7Yg3S3jivawbzVDBXxCJjXcPWSZwf+UWdWqbsgShHnW33hMPFuwb2aNm5OMUU8Ttm/5KGMoxIx+WhCktQC5pCsNUZclFldbb6Z9P4iQiw+BvGDUReSeZSZweyGAu8DpQqFE/umyUMCSYXEoY8ZPgVwbD41jt+tOOTVWLqcEVPVWON966w2/Y1fZaNQ2VVgwrnhLww36xkmXSXbEEpQm1PAGOt39016owyY1RZHuOSW81aZLXxy+vivJsy8QeGbaZzpMmpza07wgv2+9t82aFqj81P1bV1Rd3ix5l9i8yRmtTDEodKLF+zX8/5t1ll18mApDNGDGoFdU9QS2jwkM27TMOvdphoq1cbcbc/D43hvNJJRwn2whw0mmxfaGA1xxcA6XFsGJJyi6oWFhNjkeUyGtl6VjRmQbxSqpIPaMAsTvcDdNX/qvs1WfZCAp0suEysmv6KMDo9c09+etTYxCgMTxoBlKMjXEiy34BaSabGJ7YIsy2VY/wBHUuXUcEUf2zqWtBERe/8A/wA7MDU0af8Ak/UuFq4gCJsftwAQPECgkutfH8zXZxMTqYgfxKhYDzSwI3UZuWJhwrGWzHFwAACF0EIOJ8P/AOgBCgdg98//xAAdEQADAQADAQEBAAAAAAAAAAAAAREQICExMEBB/9oACAEDAQE/EKPX97j2CCWtWUpSlLxpSlKU7Jk1sePguHnNO20h65IpSlHq3obtPbZtKUomxvl5iRCEPTn0dHQmh9vl1UTy568H9fETyi4dylylLzXoQ6ILKZNeUpefhFKUggfC8khqCRNT6WPGekP8HjLj+4tXiyopT2PjUXOhTmvCExnr8P8AC8PeTaUuzmvCZRnsZCE+iEusTEh7fgQl0trIeny65I8IuVFPYpSlKUpRMuXP5iPAmMpNrnpT34Tf4QaIhP4D5LV7iyYe8z+K9JkZGX6E4o/gnlf4hIouD9PssRcTKhj9/NcV7kFhRuylKX4LihFLnrIT4rFiEy8PWLksYtQhe8f/xAAeEQACAwEBAQEBAQAAAAAAAAAAARARMSAhMEBBUf/aAAgBAgEBPxBIogioorii1FFFFFFUXCKkkUVFFC/0JLK8K8hUKKKglNQ5LpCF5zXDeJUIyumotFloTXbwZYkYxfFll8LlvUrLGtfkmPetpUIa0FxRXxcajlQL7s3G4sX4ZntiiikJ/idvhGv4dvhGovwbcUUI2F+DbiyxZ+K0+FCvs40xyo1+DbLmzAX3ZpljhHhRfViGaY1HhR6UqSiiiiiiuP6VQzU3GXxfbH95y5rjSorjBqKKKE8d0MUvjA5qMooqKmpY+MD3hGEv4N8sa9KKKYjPpcMcOWaKioTx1XD4ctDcWJGXxsfDlvhGHwbi4cMswb4Rjpy5Z/By3x//xAAnEAEAAwACAgICAgIDAQAAAAABABEhMUFRYXGBEJGhscHRIOHw8f/aAAgBAQABPxBHAPhYPapK3LBNlBRGkpfuczUHojQgT6uMZXK/FZCLfwbK2VkKCAOwXbh5ieocymcvxVwpA8yiZzBCNvV4H+yID/MS3B1wxjvGLSklNBfqCF/0xAKcOQloTOCDzNHL9y1pnOnuXEIdUxDqeyJsvYPmGNx8y4Y9QYQvSeZUftl1mXZYK9DArXZnK/U19yJlLqn0wO8XXfDp+pRfeIg4kzfZEU2abpKoOavU25/BKgH4U1A9fgmw5iHXrl3r/E4aPyyw1ZM4KKSkt7ht1aMCBTHXzEXxUDha4hwFtMll0pFiVaFfMq6iPiLdIznETuKnqYiHDLOLYkfJJ27TfuE17oAursysbVlhVMpDk/uObEAHBVqvTTqICANvS644U4nuKemMANS1KG2k31PlHm5O42YoYppHgO4mvA8RaoaO86S+oBoFY0+HZjPrgP8AqitP0Thv0xOUQ5F/sh6/3BHQfcD1/nC7/eC9mJalQ8+JQVKDVxBVBLUCv1Goh7ybFqH1BgD/ABQC15M5i8kdQOVpP4laCyqfUQVSvbE8gfmI5mCwv3G8D6lOh+Ce9+oPlfczsQS36Oj3G4adi728Kc/0Sz2RcvVfZUKmidQmyKRMHrWmOO/ZU0qSl0wB7U86D9Vn3L/hjF3DOuB9ygtYdtAH6afqb8uEKqqfB8eoLNsiAyJyhwfkh+kIAjXalQJRxX4OOJlyjxPQRbgH6lsoWsNESZWwbxY6uJUYiVBHhhnjByVbcOcr3AIrS/xPQQAytYQFSiUeJUrJRxCFC0MquXKEX2EHpeDpieZQRaZvudM2Zt1gMryhmwpAD4u/5hXrAvtUB7iuwVvWJ9fyQUEL9NGV1go9xZa0LiGziKIilKZQ6LRTyM4TSCVAI7JWd5DggZMhpBUD8DL/ABf4c/kI+yv8x+I8bC7xCo2L5ag3eF34vScatxmS+9vuAOXebJ7WEdbtv4JcIcflM/Bx+CVLn8q5oLf6h+uBZm3xhvks4iBYXuLe2Wq85lqN6t4ONmyIeTdpEi1W22heOJbN84OEUtA9QSAhKXl004U+GD1MLoFyg0dDvPmEYhvXUWqK+YyEKZCvCrV6ixnTURZ8kuDB/Ff8eJfuJRdF+yhlAD3Xc7zvTBYc9QxXl0zw0FXK/wDuY7/mOZJSe3/XKYEI/wDA4j+HUQY0X85SN3rrdS7HYPsBRrzmu4wwN67OFT4riH01CV9G0Ww21jBegEt/w1K86iiNYbAG2i2tlxumjx69+YawNCxqstZ1liFxZfD79w093aN+b/gYwgyz8LsuXFgyihcQ+3+ICXl9EA2r8xKP9o4D7IiAv6S7f7S1rZ56gtqs9w+CpP5Z8fgYw/4dRS6JxuAGFGBaomDewKNAvUBd8GMMFM1VQClLy/fmX1cNUs0A1oHhsAbSFuuVeuH1zCndDvotPWr9TUXZV0KrN0IPAn3jqi2hFUwbqktnoL5jY0urFAHLsH7lnAKgm1tebuDNWWK/xPT+FhGH4MHYuQZXZTq+klxwJbYD3UQmFfCcwCBp7uYCPJ4nyP2iKPfluJWszqKklAG/KXGH/IXKyydSk1g+BZG6EonDUbqCNQOymywiAWlNF7vlSgen4iw9RFZrWfEuwnNERQerTk9CWVtqgRKXevWFThqqoIGuGBr3LhiY2vgnnanlCXYlCyUXyKZHOEh2EC9hKyjZhc6SgNPINc3bKtZXDkL3BjBjO5efhhL2e20/X/eLh/UI7N/3EE6LqK+QoJyAWrDxLqXgUvhgPBv2y00InXkP/C5cIfhdQjPmX1OthkDsOIO/hbJyNIal/UVQ2pAt5fpLMCTowygr8CLCdQN/Ax/DBHrWK6vBKBxXiZLfnxKsWeLhbWp4mHAnBjPn/cS5NweZcjafqIiSshN/BHI+YQZc5y7A4xpukw8RDUw4xQuAVn0SyiVgqqYsiFL5RGvkutLb1Do+wQE7Ngpgem1p0lo9Y2ettepNBGUC0Lc6t7R3zXMUJgIZSVtD06lIUwNeI0KOTwWt5GOMs2UZUvoOGtRJylN/KxnH5OPwfg/DM/WUPof4nC0/HMFZF9VxGOQSnJRW0eyWhUp86y+8lh4T+JmMf4l1hyn6jCHMeJ1+OE6lwZcasa0bPTCxfIwb8+YuGFJCh4PECwC5aEraqxMR5lkQ64oFfEXLDaqK+2pprlGrVq7xZNhei1sJSLVzs+YSgRL5vXebgSiHlp87sTUVOsJR4VbCdQjM/Ay4Mfw3cqzny/8AUEsaX2zQFfELQKK4CWrbKeUhRCdvMJ6D+Z52nDKpiISgblv9y4S9lwhdxl7GvEHZc6l9VChBphiy5wnX4dIXcZcPwsGXLgy5crXjteVR08YvMVEHvxKVNucQ2N3r4+Zdyrc0T/xbDeMR15IRl0LUDcuvyOxaZdx5hseTUXZ7QCKt74udDMx+WiIPKkAasZ2OYaVseq65g24PLuBbofUYjWilHBu+JzTK6SkNUXPwafiHwmRlMLO8CvUewRyjtVrzuan9xfWhzPXmJMVEPP45/wALgGtsenhfbN7Y83oPFspuqdkV0gElRSi7bB/U+/x1ByXB2d/kaIMqNLU/hZ4wfFw6ckOAhGKfMt3XwafcVloI9RfKehn0cRtFvx3KHP8AwI5HmDUWK2L6iL0j3CHeAP8AMCCz8IlNoFjiUy43HgWBhCb0LEmcUKlQ1DQu8LgnDsclizBpSxs4ggxoTYENXE6CNRVCGdYrz9FnNApfbdCFHKFxXwPYUW8gFR3zFqpI6+qqICPmG0RyLD1rFCaWewgE3IWCiJaqpaleJbrWINhsxHbTpiEibScAyilp3xLcmv5H8HCDLnMX8CHt5T6/7lE73xMWqv8AMxCx4OpoArsK/mUuQ9psqSh2K/URNL8zCAXbr1UfKCy9/BywhkeIqgkJM6Tz6ie/AMNAEapq+lMqc6AK3Yd+Y4qrQu2KGgtvOHmwnTZxGi3NAoIcZTBYgbE5tV4Qv9S4S8qSFa6BG3qVRm9BWb2ypTXIkfcD0LQ7GoXcEFImeoBzJrnCKvIVgfxqFHNlRyDUh4NJxiJ5GL8WEWmcJwhxLgxhFg4/CVLVWHoWIYB6sRJjw36mHod5GjavqsjGZo7brxHazba9QRhZ6fhcjDlJewqpYS9hzzLi+i0UBa2rlBPBCC21G9fxD8uxLzgWSK1uryDExrW3Eeqfmbdr7RjiXtngx6P7ul4hSzh0D01BGb6yZWOx9VHzQTAKVKC90qoPSjpRzIC26M3WUUlTk9EKuLlKgJINjAVBWUF1eUUqcCsHaw5oAorIQMeIsWDFz8XCL7/DB7r/AKINOKmqN9QuU1ZA5dfVxAqHt/UdK2cbAanwvCUrrq5+X4E0DYrKK2ofUEN2ISDNBsFLyAZ3DYREs5B62pq9gjiKqKlxCK5NhyFRzs6mThflYHUusIs17AORchOELB0doAssRGvbGDLD7laUUK9cmxdWHtZCpFFQkJtSlaZ6pU7UlacO8QDaBAaxASmoO3vGRR5sjz+DzD4nKLh4jCDOSXOEG2dQ4l3ByWEvISWq/wBUdKInWcRkrsS6NbS22qlFDbOb5lvNTt7noisot54ggKoMs6jPLWfTFevEMFQFNA7VdWceLj/zKgGoQsAJ0nLAqdiX1rfBVFcQ1X79Xy54u+1q9mQpAMstMQhndtss/YCjdmFoa7rDJqeEVqQNeqFEwbXvx+XV80lmS/ZFpxw0LS+c6zJawieO9b8tHoJSIEhQ2irUBBBqDTxLjSWThiFl1L251DxAUAC1WgIWFhCBfGrBAIosRsSXtRAKtAmrR6gvx8scXXNX3K17pxFzdqKiZVXq6aq6PObkdOQEq0ss5M3Yfg4iXDxwp2k4yZDLWXKtoWddMGlZUFF07yf/AAmFty3xlxlG32M/1YLuDI4jrZpL2cmL8I7NuXs0jxGEup5Q4jxcvzLi6YqIGAc6iMmBhTqlUU009ouKE5FRNCNnQHqVRJry3Cvbcepd/MW8HdHOLzcu16CWw80BBxw+5d3pwUoI4bHeaFuWHK1OFQ+g9BEGtKlah7qWC+ODxOowjdQr/PG+beMjiy+VMHkIBgxSWsXFqiFjQA91kp8woNrbx1MdWq/TEDAbsTylal08zHcEhXNyyL7II7F2XtwYU4l2EGPMrIxRUGGxtDkGIlI/Ux6cJX9Cw9Ql8QBAh4AB8LBbWAFsF3Rh6hkdKNglj8iDAwDmC3jfiB69w2XY85zEAVDshB2+DFPhiE9ExPscwefyITR4vuFHHyxgBQlOuZYqWbOEgB69xTDMvCO+cBUNuJaLa+vc6KxQsVyB3Wg2jim+K6xlF1EMtvZ5Drn7gl5RDPJzX1DiIh4yVaavvHmbyAUyfppvsYUKsBkUbvyvHCbrlh4au/OccomSYipPXDR6CPLfilmuDyd61BDEzQR48T8X7ighAOzOVYL6SARUrsxt6W+OUpYXtTq/RmcIRiJ1a8JpT2SUQNkVxQjCubC51JdTyuCm7V1DKRTPDkNF+Ujf1AOQDquzjh6mtcDR2LYmcDIXc4C6FwUVTyc9zsODGaATmp2nz4j1RJdCnix3fMoQzMtnK0u36VCPdnP66KrwhXlEkTeCiqeo8KobglDi1O7KgXAmpTxWvm+YswAKlHKtXbxw6iHI7NbxFvjfwTlD4X/dLt69MMWfYRHn6tqXraJ93KFgO7P3g2oZx5gcLDmmKKEOLKiC2rVgIOK1epmSpQDSpxaDKt/qVyFuLpoz5Bw6SZ05/qRsq2ucxXiwoGlJdqgl5uwC9ZbtVbaWxfT+O4aTlOFQnU5Rhuwe6j1KDCoMrLI8Ra4hzOYMqIN70LijEdWiLpriUy3dvAJ4SF0cXTsDIbALlX137m2lqVShysjqG7lkLjZl24Ho3Fd/sjog3/EwX3PqA89AuPGb12jBrQFN8rNMyOQ8lUI0+avb5lerUqV2P2AOLqZ/MpChU4Ku68PEWk5vPWg2sVK3Vcw3NaqE2DotUeJf8/g8jzsOZfUHJpYdkXTDi4pcFxl3qHmLqozhf4Wxj0J7Saa5i0KL8wLfYY6jRkGXpdjIcwgLb5/umc209Qyi2/uAEOTh8QpBOtgVq51E3jhasPo8ThrHfh9SojRWvB7iMGV38XUNksEd0h4jFKON7wq/manyijaCodgADxA8dI0DT08I7gmi3JBXTje003CUpb7Kbn/YoISUlFr4dFFmjoiRrc63SBQKrpoalE1khgEdW2K88pFFIa4K5gV5ICurXSKLpQjoeYwqDlqUJEVwBDviLLRkE62KUjKKFkcxTi5VLcJUdJjJygzlhwjOUNY9jx2t1fcudC81sG1vsIWlg8EaKlbySujl8rKcXntHSso6vYjRgm3BdNeG7Aa3By/A7NlMRFslEYcwATw8IUkInShEPQBwe3zOrK5FmFfHDO4NsuslXI0b+yAghwttAD+CJLJqjcRdCwfRGxdwLAYHAAZxLRs8i9HR5Tw1e1cRFUYcoFiZeQhFmjw3T2y27L5tg8UEDhGBGxSadkD2MVMGkVoz7luO1c0AH9RwuGJcecnDCdxnUI9qCOvVX3BAa52iUUIlcjxOnbeYIaq65NlOwXbtt7PafucHu/OMamrTCRSGvqckagqUGXtgDL5vZZmz8kA8JzdBKSND6Jo5PupQQyPEG03i/V1A7NVb3Ci68Vk9LnZu95cRnStced58KheXGx0zO3XmXx9174Gei+a2pdzhKOl3a5Pqctj1VabSqTirbhfNVpKK9voa4q9hlqsynz/gemz2MEu7wMCudS6oEp9RNV8lExPL+KccVX3fH6mDEQPIV0PSk9yq5qVvwhJ1bb1MazyQ7w9XcvYgJ1c4LzsK3QhdLy3c2Dxl7tqKdr6l/avqvuJgsjqzQ6z3ZcWzSVFDe29ZvcQh2pAvp8e9eIWslK9gYO1/KtQB2MgcT6POVU4aaOU8DavkS5ydfV34A43bmw2ciJ3IP+aDYFvUwEFl4XAF3Y6yKLYK4upa1JXm9IVXH8yyAGIgcS9Ter9SitmmOS7YOy9ZFwjUWqRhewq3jmH3e6TV4SZf6jYCJxXgCD15lfBwdWKGq5dHpKOCV4SChSS+S18jX/aKNieAW0aotgLvUqsfuVSRbIl2wTE2Xoy9zmCVTB9xZefghzDmd/g5inVPi9wBaWeL/mLKX1zACtGcXBHlqAKA13ct4/uAm2zqCdG3HqUGFIv9S0uKXAfwHXYORdIuQnUAhfk3Vl8RtV2rUouLQvHzLGeoyyiCUGnu5lV/kYV4CvaGSIBF1235bf3HaqakNMffzH1KKTa97hfuv6RVXhYMcuDAPwIuXEpNnDcHYowMgpIczGMgWOH7l6lfSEtohIiBEfLxCPJeajZsaeEn1SwBozgOJfwerg2vJ/ROMQ2CWIz1ca5plRK6hiYAcxw+JwYSqLDQIB5FPBB5nlJwk89/NHlq5YUEZHNhOWtFMu8udo4mGuwJSRZD1Aga1OE6IS9ix9RalnpPKWOXD6Iqwe8sg2Jj1AtAOGL6YG6F3kmR0lUbuuor+E8wduXH8DTDSKyJZA2HPE3HHg9wcBfFMPKs8jCy3q/JMqyvPicMQq3RHc4DsY11y52WRdINL5j1U8YR0feNbkaiJqQkt1LVabe5uthIVNFXoNbxky1hQAVe6U484ZrktBXUF+1o1wolsENW+7c1WitV5lgc/uCgUr3DiX5iy+2LlR5uGxbdRVwpLypttV3U+Bo+yGHJM7aWrql202pZavvuIuuR0eIAxDo5GBBaB2d5OGKDHmDsI4NwgEoVQWwQO6yGsVtg94IsM7pidX0wuN/++GxFfMv4retiFP6dXL1UB8XGmmgTbuuIHWNLENLjWtz1EPxjqlhK0KGgZyxjWwUb6KO7LiOtFqpRnc0LuBixpbTeuIopvtbrBEp6MIIUlvqKvkypotWQjROroIlAcHJa2yUwNaaikhiWqK9JW4PTFuWUS0luzscMri/BrFjYXm1S3XVwK1akCjWQLFVquZST68hr5KVfaDTkVeSWFhBw41NJqM4S1zlOyJcKR1lhzHrA9J1LBQpE/wDOYCd+3ygK99T3v5mkB8TBS4LeINhdF/P/AFNTQLiF7rK7uLRbMxjlBrXMw04XzGx9wyodYa+t0+JZ6fGY0/1ATwSKqqAuNg4Rc53ql37qCEpT4YLzb+4rl0Uy6Y7Oqh66hrueSK1y/QuVjvEU1O/JlVplVsu0yAXKUMBEeIncLEhwIUeZVWj4hMHFzvnJxOQY1FplnTyP3GgcMURTgp8y/ReEVuzpCKQUceyDbyeWHRTolx5GnFfEqO3YfoYFjiiiVQWL/i5ThrCixXMeXEIW9CoVbL0sjq9r8KBTx4E4RKgTVRhsmByJjpU3LhBQRTS9MZssRmy5dn2qSGVSRhpOYtkeQb8R8Ru/UNlIFpGb4Fg+F7qLXXoKLBQGxZY2wviyAtK4ALQGnDKQ/wBypasSbuwUkE4RKpv9xWAiWOxl94eyGwg72MeDs+YEIgVxkWDRb1NJdMpihtseGc0aT0f2xbClXJUUAs8XhBx7lr4hjZWI9lQeAAqsDC+UIoAVaIqE8thXuVHsHYigNCgfKuIvOiNrUV4ommKfcyYqOLkS6US2REXALqIqx4rMQYoUmQxj2VW9dQyjjFPGMR0Mm56RxbZdP+IPwBcPlg4RpRrBKzSpMeY/lRQtlce9b5+pV+UVzNNgHgh0Asu4P4xUdKJQLCLGFkpr+diTaHxMShy+YKd7d9RtnC8I3L5Snvyxd5f5nGzDEoBS27jaqGwxaB6lO0W0qaX0xNLZV1EAbg63gRjsQF9apK0HLAjw1ZiTbd9vjwG+l7ColR8a6vy3uuYDmG4DYbWPEYUFEGkZVeanLozuB3LvRgqA2xvJZM/ucdbxTCQqVYrM27xsSwALvUC8j5IWXkuBO5gi5iy+4hFIGxqpAuxu1u5h31rgWOwFq+05lLUiGt5YKuytig8/zBHIC8cYfZB3rP6nL3FAZRJZsUOeU8tBnUzHujJRKKufiDFtXxDYWbPZX8wC64GbAob5dD/1ymvBtnuO/wBULpPYFMk0A0o3sKHbCvngorjo3RXfRA4ADDIUBKPHrzOrYJIYBDh2V1xKbp6ePJo0UQqiERhdmPOBoVOXRfKwA1aohvX1Lq6QTWJeCngNhSsTzCLUeeByF22kqxpgX+2J/wDLCYF88X15llUSJMkbsS1lKIsFmXmG0W26dS9N9zeLioD5XU1uz5hAnAlXCuVrxcI4FdyyiwW9x0QajHWdRlpV1c41vzOE9k8Ff+iJryNyAFq/O7N1TKFK0XciIi065uVAp7x8nEAGw9vMR5Vv5BiyPJWcfqgL73ivcoIdgYC2PRjx8oEt9QLALzKArwEGOqnJEHoBGIN0EvJVeNTu7fc1/wDFBGwdqrfdwezHtJXhHvwQNGNwGtFAHavEQS6Kw638s3OpofMJeF3EVwTTSdFUxwhACqu+UPUxJtuZYNEBnId5jNDPpkSBd3bW6+YU8EjtGrqfIXh2I6hZxdwcCpxm43eIHsNmtKiKcNiVXzLwht8D/c86+7uBx8CxmzWz/mG2ys2Ygwc5zAKE9EreH3LWC/JKMECc6ca2cgtBJz40q+4XH4Gg1qFWNglhS0oieGq9JWo5j2HhUsHDGGHrYs720jJAPXxVtYMvOJwUa3kAcitDqh1AnKAIUW3gyNB1KBk0BkR4K9lX3HBbjFJpYCOXSvEeNdpLOqe3ha9ymvoxYanqEAcvTiUtspcrUCUuCRp8RtxC+UTxMggxp1GqyCFvcbSWsf3KAqxgNwDmDbiFIzuZUR9u/wDUcchxkVar4MGEEPzK2IWdJEPNuAxF9fsncwHJkSKFHuGZ5VHz+M79QqPiIq7iWe7K1KoPj8DuzlZGlJkPeeJCR9MfLUqHMvdMMTh4yPzJaxzLN0OPcuc1KcIRIE52c6w36gKtz1WVT7tv8Y731xBo+ycQaGe0DQj0YjhfRLvnHSOy8J9rLChPk/URaU6D4hwUWtqvcZaNTj0lqRZ0npmdcTHmCTIfiO1wwxY3JabBMQZjlqXsTicLuWjULghpi0rKXERHcUaRKmsGU2aHErVJHFbkGuufEa4D43mBxbwPaZogl5gGDnsyFwoU8wLWwrpit6L4LnohSk1/uHzTt5gqPCN+yF5TL2GadUlessdFGVJHHER0VionPPcCylI7luwVVd0Xd5BnoTLXWbK+enjJcohuJ9hRE8eaOJkGXewYpdlMdEEg6xbpFCBKU1dV0tGhWrImNFWL99KnAAJqx0Ll1FQb0Pd1F9rZCa9wttJGxy8QJ1LJFUY1aWx59Rg8XzHXfMSotnpf4gQSr1LbU5y1EijTvZSl960RRC4sYhfQp3AKqt/EpVlXmK0QJrf+IlGWeNdxtE7qcAXDh6eEIaVFzWi/pRUGspN4EoDoTnzGy1ICufAvcM88OAlFfAy57uIsjBj8QdCO3MxVXBxnK5fo6G2AXXFg16IvyiygrlsMXVLXNjEWGFjd2q+T3XqMCVLnTWq0KXGLrAoJVMuP9QPBLCD7jsM5qDswnAri/pjqsCFvdRvQry3xMHsqMIgYnlhO/VmckTSKDu3IZw/uEI0Y5zOEpfZWBALgHbPc3HmMNjBOr4C7VrjY6CiyIDgtGl0kF11SV5VS2ga8OWPw45LVEBih0+IRlBUbi9ggZ555j48QauKBLy483E4ZyhzDLIdihUgug4It1/1cZJCbTVIgdiy5DTffyFiBtRdJUc4OIAtIlHHhfB4IwhbFypyRl3aQ8FS41XzNr8K5vUq+d/UogCQb+pVwI6GyVDzRxLVbZXd7LxfEt5F+Yq4K6gPCvDvEE10q75hYVVL/AJhAO5dIs86Vx8+au4+2jAma2zUs48xKFngln6l41+tzyt3ywtVIelqPFJTDOq2RQWgA21sv6lQtXOkLAU7xkw0K+YnEFpMWR4uaIEERxAsGvtnR25oCqsGhOQpw2U0BFgU3VboNd59xB3vFCtF+DMXUKP1LzxNM5+pxg7HzsvIy0yMG2euH4gqB43/7zLWpryTgqz3fMbWiPm8i60zLlZAzmU+f5lHiL/EMSinnsmyG2LPtm/eEYVRiAdmrUZVVfc4xE9aqhSwscsv0yIzTe7lAIKnVGFAAANdZZLUKjAvFGvhzBE3WK1lVlK5PiLWEJnNIUCwQ5YzICzWxVnKzhwpvAD6dLQvUcXUXAFrAXYr+4AHWXZXvI8uodIDmPcOGPNRSfNypFuOLTzBGCg6zBq5bG63iKX2nzyxNXxB69KqrYfCsNhfuDOSiAAWMAcPniHrBdKEqstAWsuPM90fEaOS6YNkXEd/A6XGsOH+lHgJ/qBOOmPUTtaoq/Ew+rviNtrrrZ7v5iXVOlTiXguWGtwP4h0zUOxZ6gEjWquIaANAqCgKNcSro3ywA1AWWXlDByJmqINU03am6ihoXA4AKvBPY3DTnQKykslWJ9QFNQkAZRA5yK6dkF1ViANnYDw061Aa9w7OLcO5SFuDjW5A68mY+4vVx7O9cn3SIn/R09/AcMOVZuoy+bXl1xkr6sWFVfDMzqH0URC4AMCHM0nmNkb7UYOvwX3OXM0nzLBTgpOdRbTXNxONruUl7vENmKESnluIUbTcitv8AkizeBx5uXETYG1Kh3e3wQRgqNrKhxMIchKjYFyFVbqKxGV9UzAsu+IqWqS6OR/ew2vcm8R0DQ93HUMvdiuBh3UzWCCwK7b55i8WL0tYNCgUA3tvcccdI7pivJ6l8ptiZGFTUuufGFC6A9xPg6EzI2WWWclQk7h4NOuFazBk3EtXE0zYHRiNhKmnpDVfg9Esxq61CBbxGeAUw9u422Ck8w/St0qKgSIFCxuQA5q/Mv/5Rt6kFsUNjHP8AcRB7/wCIrT4hzALZZgNFfWT8wk5TGi6FlQNOHiNF1MDaLH2vqVvTJQotihm+uLZidPtrGlsw6Pu497KjnApbjnL1iQ5L/HnE1Hqj3Ey5+8KiyVS6XgLQCr0DLQJl9QEK+T47lCbRjTVYKtuzKvYQ0y2pwn+ufUu4vq4y4hagwSomsipanuji/wAFpCq5syn+1KF5zFO03NgEK16IciQktdCsPyQBVjDksreHnJWeNbCpY5NmIE8Io4gvzhXiYNLzazdG127hSg0K+QZr/KLylJDZWu65HK9zOQJPY0E9HI4j31vcHIcgpwzUeI5FPROFTkxfwX1Kxe08CaDbufcMpJEFA/sHlzUBGYsqbUdqDXqtgWaKHgbcRVdrOCYZ5IA7NE73mYX9yxKGwY/EbR8kJEijsd5ZYInz7ieHh5rIqMVLWws0YBBFrZv4l+vtYgNXRnwyq7csCgxT+ZyuLSdRaFQtPMOWDcuKFi8JUy6LntFprwx5uPMKecnqZ+AZdE6sQp6h7ILahS7leQxOUGj3KvOp/aIvEXu5qxb213ORx/mGzldVFL1MiLm8AavzLrKvsOoO6+V/cGcRgYlxS49/i8YRn4KXGXkZUouTmLNMefie47DzOdy7zn+Gg3zD2E1FpyY4yl8yxZ22ABA8f3EQtr1FME93CPA22vEpejniHRVjPIx8Q3KpWUwwVbhUw0qz+2YyGhqr6lRFDswFit3dL5ziMazACewtvjx7hHNAd7tfUoLN5jVdVOgedcP3cGCIhWq6Jw3WNe4DEqSd9GqeGR6VRnu+HAb9k2mj7FSTWPJa6gHNJXpZptAI7VVDK8Z1SDkfI1TLMsi3aBJ0GiaXo13mK1UBO0pZnhXyHqLz7qSsjnBF4PEBfTgAu0+KYjRLGVV+YWYeZeGj8H5LeenM4Kgaq8Fn+UbBpQcHk7hpvuUgdYBp5549wqEdKsf1F5inRKIC6WpVEv8A6lhSFzxHiIYqqpUaLb2BFa4HI2y4ptniK7Axwp2Cgphp3EDF+NhXmh5GJaUcBfMR6fN13Gs88/3HLQ6sa1MDGE24kYMgoCqoea5r3EhraC9b80+I7lWBR2j5VfuC1UAxSu882/olA2Xcp46rExOE5mumQSoRRRdoYjB+VYMQSGx3dXNS/OqZYoEtqC7+pwOIjTWuxbeTMYwCtCaHyZz75j3dAORw2N+55RFqnjDTDHxKhC4BJWq/Bc4i2xacLbaD3ByfKOtg9w7S1dqBG/M0MaJcB2sipEcxi7Rf02iVpKviolvAfETA4VXEVRtWRFXRe6lm/wCYZi4ergHB7fEOb0Ye4kKxnL+DK7NSQNTzdeivMKSCxRpFHrUvpfUSrIIka4JW3sEN7odEpTun6TazAYtwJpLkw4BMm6qcLOZoZHsYW+B10h4XyvuLY3+GhwOCz7T3CY+c2A2hjddjF3+PTYot/E1X4XkINXcdXPlpyVcQU1MH1PEoHqEBFk19s4Rb7YgMHVwd3DwQAtuuo6vMPNz2v1LTQ+rZhaVdyVenGeJSMz5dTOwYT3BXLaOoO0uvUIJo9ZEMgtiq6eLjh6TBFtXO2JFYhAKh0aHbe5UginJsfYYAPKGQEIA4pBPiEJIQbpnlz/aixyh4TB/qPLjWLR7itXNK6gniNPHcrsvsfEtN9w044jpS9nNkPGfP0pX/AMiXatPzUoHbL4GXABxHdvKV8/3Od7qZNef8T+M/qcGPEZxTlO2dzlOT8jzP6Jyw6nAix8zlHj6j3G0j3Oo8TkhBzOSJpnX8g5fZP/Q8pwfE0L3iZWsnB/E4n//Z"
    #bytes(request.GET.get('imageB64'),'utf8')
    file_name =str(uuid.uuid4())+ ".jpeg"
    with open(staticfiles_storage.path('uploaded_receipts/'+file_name), "wb") as fh:
        fh.write(base64.decodebytes(data))
        #fh.write(codecs.decode(strOne.strip(),'base64'))  
        
    text_in_image = "I like to eat delicious tacos. Only cheeseburger with cheddar are better than that. But then again, pizza with pepperoni, mushrooms, and tomatoes is so good!"#Api().getTextFromImage(file_name)
    ingredient_in_text= Api().getIngredientsFromText(text_in_image)

    return JsonResponse(Api().searchRecipeByIngredient(ingredient_in_text))