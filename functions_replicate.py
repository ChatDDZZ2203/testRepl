import replicate

class RepliGate:

    def __init__(self, api_token):
        self.replicate_client = replicate.Client(api_token=api_token)

    def define_version(self, model_name):
        model = self.replicate_client.models.get(model_name)
        newest_version = model.versions.list()[0].id
        version = model.versions.get(newest_version)
        return version

    def get_image_stable_diffusion(self, prompt):
        result = self.define_version("stability-ai/stable-diffusion").predict(prompt=prompt)
        return result

    def upscale_image_real_esrgan(self, image, scale: int, enhance_face: bool):
        """
        Specify scale in range 0 to 10
        """
        inputs = {
            'image': image,
            'scale': scale,
            'face_enhance': enhance_face,
        }
        result = self.define_version("nightmareai/real-esrgan").predict(**inputs)
        return result

    def get_image_waifu_diffusion(
                        self,
                        prompt: str, negative_prompt: str,
                        width: int, height: int,
                        prompt_strength,
                        num_outputs: int,
                        num_inference_steps: int,
                        guidance_scale: float,
                        scheduler,
                        seed):
        """
        Returns list of urls to generated images

        width and height:
        Maximum size is 1024x768 or 768x1024 because of memory limits
        So be careful with 'width' and 'height' parameters
        Allowed values: 128, 256, 384, 448, 512, 576, 640, 704, 768, 832, 896, 960, 1024
        Default value: 768

        prompt_strength:
        Prompt strength when using init image. 1.0 corresponds to full
        destruction of information in init image
        Default value: 0.8
        (I don`t understand how to use init image with
        replicate tstramer/waifu-diffusion api)

        num_outputs:
        Number of images to output.
        Range: 1 to 4
        Default value: 1

        num_inference_steps:
        Number of denoising steps
        Range: 1 to 500
        Default value: 50

        guidance_scale:
        Controls how closely Stable Diffusion will follow your
        prompt when generating images. A higher value will force
        the AI to be more strict and follow the prompt closely,
        while a lower value will give the AI more creative freedom.
        Range: 1 to 20
        Be careful when using extremely high values like 16-20.
        Default value: 7.5

        scheduler:
        Allowed values: DDIM, K_EULER, DPMSolverMultistep, K_EULER_ANCESTRAL, PNDM, KLMS
        Default value: DPMSolverMultistep

        seed:
        Set 'None' to make it random.
        Search on Internet to get explanation how it works.
        (I don`t know how to explain it shortly)
        """
        inputs = {
            'prompt': prompt,
            'negative_prompt': negative_prompt,
            'width': width,
            'height': height,
            'prompt_strength': prompt_strength,
            'num_outputs': num_outputs,
            'num_inference_steps': num_inference_steps,
            'guidance_scale': guidance_scale,
            'scheduler': scheduler,
            'seed': seed,
        }
        if not prompt_strength:
            del inputs['prompt_strength']
        if not scheduler:
            del inputs['scheduler']
        result = self.define_version("tstramer/waifu-diffusion").predict(**inputs)
        return result





