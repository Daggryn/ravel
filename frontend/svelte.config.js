import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vitePreprocess';

const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter()
  }
};

export default config;
