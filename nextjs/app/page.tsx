import InstagramDMForm from '../components/InstagramDmForm';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500">
      <div className="container mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-extrabold text-white text-center mb-8">
          Instagram DM Sender
        </h1>
        <InstagramDMForm />
      </div>
    </div>
  );
}