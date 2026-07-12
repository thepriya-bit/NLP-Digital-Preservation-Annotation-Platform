const Navbar = () => {
  return (
    <nav className="flex items-center justify-between bg-blue-600 px-6 py-4 text-white shadow-md">
      <h1 className="text-xl font-bold">
        NLP & Digital Preservation
      </h1>

      <ul className="flex gap-6">
        <li className="cursor-pointer hover:text-gray-200">Home</li>
        <li className="cursor-pointer hover:text-gray-200">Dashboard</li>
        <li className="cursor-pointer hover:text-gray-200">Login</li>
      </ul>
    </nav>
  );
};

export default Navbar;